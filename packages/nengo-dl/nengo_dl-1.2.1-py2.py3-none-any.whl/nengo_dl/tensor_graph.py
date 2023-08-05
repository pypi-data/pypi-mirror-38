from __future__ import print_function

from collections import OrderedDict, defaultdict
import itertools
import logging
import warnings

from nengo import Connection, Process, Ensemble
from nengo.builder.operator import TimeUpdate, SimPyFunc, Reset
from nengo.builder.processes import SimProcess
from nengo.config import ConfigError
from nengo.ensemble import Neurons
from nengo.exceptions import SimulationError
from nengo.neurons import Direct
from nengo.utils.magic import decorator
import numpy as np
import tensorflow as tf

from nengo_dl import (builder, graph_optimizer, signals, utils, tensor_node,
                      config)

logger = logging.getLogger(__name__)


@decorator
def with_self(wrapped, instance, args, kwargs):
    """A decorator that can be used to ensure that any ops created within the
    wrapped method will be added to the TensorGraph object's graph."""

    with instance.graph.as_default(), instance.graph.device(instance.device):
        return wrapped(*args, **kwargs)


class TensorGraph(object):
    """
    Manages the construction of the TensorFlow symbolic computation graph.

    Parameters
    ----------
    model : :class:`~nengo:nengo.builder.Model`
        Pre-built Nengo model describing the network to be simulated
    dt : float
        Length of a simulator timestep, in seconds
    unroll_simulation : int
        Unroll simulation loop by explicitly building ``unroll_simulation``
        iterations into the computation graph
    dtype : ``tf.DType``
        Floating point precision to use for simulation
    minibatch_size : int
        The number of simultaneous inputs that will be passed through the
        network
    device : None or ``"/cpu:0"`` or ``"/gpu:[0-n]"``
        Device on which to execute computations (if None then uses the
        default device as determined by TensorFlow)
    progress : :class:`.utils.ProgressBar`
        Progress bar for optimization stage
    """

    def __init__(self, model, dt, unroll_simulation, dtype, minibatch_size,
                 device, progress):
        self.model = model
        self.dt = dt
        self.unroll = unroll_simulation
        self.dtype = dtype
        self.minibatch_size = minibatch_size
        self.device = device
        self.graph = tf.Graph()
        self.signals = signals.SignalDict(self.dtype, self.minibatch_size)
        self.inference_only = config.get_setting(model, "inference_only",
                                                 False)

        # find invariant inputs (nodes that don't receive any input other
        # than the simulation time). we'll compute these outside the simulation
        # and feed in the result.
        if self.model.toplevel is None:
            self.invariant_inputs = OrderedDict()
        else:
            self.invariant_inputs = OrderedDict(
                (n, n.output) for n in self.model.toplevel.all_nodes
                if n.size_in == 0 and
                not isinstance(n, tensor_node.TensorNode))

        # filter unused operators
        # remove TimeUpdate because it is executed as part of the simulation
        # loop, not part of the step plan. remove input nodes because they
        # are executed outside the simulation.
        node_processes = [n.output for n in self.invariant_inputs
                          if isinstance(n.output, Process)]
        operators = [
            op for op in self.model.operators if not (
                isinstance(op, TimeUpdate) or
                (isinstance(op, SimPyFunc) and op.x is None) or
                (isinstance(op, SimProcess) and op.input is None and
                 op.process in node_processes))]

        # mark trainable signals
        self.mark_signals()

        logger.info("Initial plan length: %d", len(operators))

        # apply graph simplification functions
        simplifications = config.get_setting(model, "simplifications", [
            graph_optimizer.remove_constant_copies,
            graph_optimizer.remove_unmodified_resets,
            graph_optimizer.remove_zero_incs,
            graph_optimizer.remove_identity_muls,
        ])

        with progress.sub("operator simplificaton", max_value=None):
            old_operators = []
            while len(old_operators) != len(operators) or any(
                    x is not y for x, y in zip(operators, old_operators)):
                old_operators = operators
                for simp in simplifications:
                    operators = simp(operators)

        # group mergeable operators
        planner = config.get_setting(
            model, "planner", graph_optimizer.tree_planner)

        with progress.sub("merging operators", max_value=None):
            plan = planner(operators)

        # TODO: we could also merge operators sequentially (e.g., combine
        # a copy and dotinc into one op), as long as the intermediate signal
        # is only written to by one op and read by one op

        # order signals/operators to promote contiguous reads
        sorter = config.get_setting(
            model, "sorter", graph_optimizer.order_signals)

        with progress.sub("ordering signals", max_value=None):
            sigs, self.plan = sorter(plan, n_passes=10)

        # create base arrays and map Signals to TensorSignals (views on those
        # base arrays)
        with progress.sub("creating signals", max_value=None):
            self.create_signals(sigs)

        logger.info("Optimized plan length: %d", len(self.plan))
        logger.info("Number of base arrays: %d", len(self.base_arrays_init))

    @with_self
    def build(self, progress):
        """
        Constructs a new graph to simulate the model.

        progress : :class:`.utils.ProgressBar`
            Progress bar for construction stage
        """

        self.target_phs = {}
        self.losses = {}
        self.optimizers = {}

        # create these constants once here for reuse in different operators
        self.signals.dt = tf.constant(self.dt, self.dtype)
        self.signals.dt_val = self.dt  # store the actual value as well
        self.signals.zero = tf.constant(0, self.dtype)
        self.signals.one = tf.constant(1, self.dtype)

        if not self.inference_only:
            # this variable controls behaviour in the simulation that is
            # conditional on whether we are doing training or inference
            self.signals.training = tf.placeholder(tf.bool, shape=(),
                                                   name="training")

            # variable to track training step
            with tf.device("/cpu:0"), tf.variable_scope("misc_vars",
                                                        reuse=False):
                self.training_step = tf.get_variable(
                    "training_step", dtype=tf.int64, shape=(),
                    trainable=False, initializer=tf.constant_initializer(0))
                self.training_step_inc = tf.assign_add(self.training_step, 1)

        # create base arrays
        sub = progress.sub("creating base arrays")
        self.base_vars = OrderedDict()
        unique_ids = defaultdict(int)
        for k, (v, trainable) in sub(self.base_arrays_init.items()):
            name = "%s_%s_%s_%d" % (
                v.dtype, "_".join(str(x) for x in v.shape), trainable,
                unique_ids[(v.dtype, v.shape, trainable)])
            unique_ids[(v.dtype, v.shape, trainable)] += 1

            # we initialize all the variables from placeholders, and then
            # feed in the initial values when the init op is called. this
            # prevents TensorFlow from storing large constants in the graph
            # def, which can cause problems for large models
            ph = tf.placeholder(v.dtype, v.shape, name="%s_init" % name)

            if trainable:
                with tf.variable_scope("trainable_vars", reuse=False):
                    var = tf.get_variable(name, initializer=ph, trainable=True)
            else:
                with tf.variable_scope("local_vars", reuse=False):
                    var = tf.get_local_variable(name, initializer=ph,
                                                trainable=False)

            self.base_vars[k] = (var, ph, v)

        logger.debug("created base arrays")
        logger.debug([str(x[0]) for x in self.base_vars.values()])

        # set up invariant inputs
        sub = progress.sub("building inputs")
        self.build_inputs(sub)

        # pre-build stage
        sub = progress.sub("pre-build stage")
        self.op_builds = {}
        build_config = builder.BuildConfig(
            inference_only=self.inference_only,
            lif_smoothing=config.get_setting(self.model, "lif_smoothing"))
        for ops in sub(self.plan):
            with self.graph.name_scope(utils.sanitize_name(
                    builder.Builder.builders[type(ops[0])].__name__)):
                builder.Builder.pre_build(ops, self.signals, self.op_builds,
                                          build_config)

        # build stage
        sub = progress.sub("unrolled step ops")
        self.build_loop(sub)

        # ops for initializing variables (will be called by simulator)
        trainable_vars = tf.trainable_variables()
        if not self.inference_only:
            trainable_vars.append(self.training_step)
        self.trainable_init_op = tf.variables_initializer(trainable_vars)
        self.local_init_op = tf.local_variables_initializer()
        self.global_init_op = tf.variables_initializer(
            [v for v in tf.global_variables() if v not in trainable_vars])
        self.constant_init_op = tf.variables_initializer(
            tf.get_collection("constants"))

        # logging
        logger.info("Number of reads: %d", sum(
            x for x in self.signals.read_types.values()))
        for x in self.signals.read_types.items():
            logger.info("    %s: %d", *x)
        logger.info("Number of writes: %d", sum(
            x for x in self.signals.write_types.values()))
        for x in self.signals.write_types.items():
            logger.info("    %s: %d", *x)

    def build_step(self):
        """
        Build the operators that execute a single simulation timestep
        into the graph.

        Returns
        -------
        probe_tensors : list of ``tf.Tensor``
            The Tensor objects representing the data required for each model
            Probe
        side_effects : list of ``tf.Tensor``
            The output Tensors of computations that may have side-effects
            (e.g., :class:`~nengo:nengo.Node` functions), meaning that they
            must be executed each time step even if their output doesn't appear
            to be used in the simulation
        """

        # build operators
        side_effects = []

        # manually build TimeUpdate. we don't include this in the plan,
        # because loop variables (`step`) are (semi?) pinned to the CPU, which
        # causes the whole variable to get pinned to the CPU if we include
        # `step` as part of the normal planning process.
        self.signals.time = tf.cast(self.signals.step,
                                    self.dtype) * self.signals.dt

        # build operators
        for ops in self.plan:
            with self.graph.name_scope(utils.sanitize_name(
                    builder.Builder.builders[type(ops[0])].__name__)):
                outputs = builder.Builder.build(ops, self.signals,
                                                self.op_builds)

            if outputs is not None:
                side_effects += outputs

        logger.debug("collecting probe tensors")
        probe_tensors = []
        for p in self.model.probes:
            probe_sig = self.model.sig[p]["in"]
            if probe_sig in self.signals:
                # TODO: better solution to avoid the forced_copy
                # we need to make sure that probe reads occur before the
                # probe value is overwritten on the next timestep. however,
                # just blocking on the sliced value (probe_tensor) doesn't
                # work, because slices of variables don't perform a
                # copy, so the slice can be "executed" and then the value
                # overwritten before the tensorarray write occurs. what we
                # really want to do is block until the probe_arrays.write
                # happens, but you can't block on probe_arrays (and blocking on
                # probe_array.flow doesn't work, although I think it should).
                # so by adding the copy here and then blocking on the copy, we
                # make sure that the probe value is read before it can be
                # overwritten.
                probe_tensors.append(self.signals.gather(
                    self.signals[probe_sig], force_copy=True))
            else:
                # if a probe signal isn't in sig_map, that means that it isn't
                # involved in any simulator ops.  so we know its value never
                # changes, and we'll just return a constant containing the
                # initial value.
                if probe_sig.minibatched:
                    init_val = np.tile(probe_sig.initial_value[..., None],
                                       (1, self.minibatch_size))
                else:
                    init_val = probe_sig.initial_value
                probe_tensors.append(tf.constant(init_val, dtype=self.dtype))

        logger.debug("=" * 30)
        logger.debug("build_step complete")
        logger.debug("probe_tensors %s", [str(x) for x in probe_tensors])
        logger.debug("side_effects %s", [str(x) for x in side_effects])

        return probe_tensors, side_effects

    def build_loop(self, progress):
        """
        Build simulation loop.

        Parameters
        ----------
        progress : :class:`.utils.ProgressBar`
            Progress bar for loop construction
        """

        def loop_condition(step, stop, *_):
            return step < stop

        def loop_body(step, stop, loop_i, probe_arrays, base_vars):
            self.signals.bases = OrderedDict(
                [(k, v) for k, v in zip(itertools.chain(
                    self.base_vars.keys(), self.signals.internal_vars.keys()),
                    base_vars)])

            for iter in progress(range(self.unroll)):
                logger.debug("BUILDING ITERATION %d", iter)
                with self.graph.name_scope("iteration_%d" % iter):
                    # note: nengo step counter is incremented at the beginning
                    # of the timestep
                    step += 1
                    self.signals.step = step

                    # fill in invariant input data
                    for n in self.input_ph:
                        self.signals.scatter(
                            self.signals[self.model.sig[n]["out"]],
                            self.input_ph[n][loop_i])

                    # build the operators for a single step
                    # note: we tie things to the `loop_i` variable so that we
                    # can be sure the other things we're tying to the
                    # simulation step (side effects and probes) from the
                    # previous timestep are executed before the next step
                    # starts
                    with self.graph.control_dependencies([loop_i]):
                        # note: we use the variable scope to make sure that we
                        # aren't accidentally creating new variables for
                        # unrolled iterations (this is really only a concern
                        # with TensorNodes)
                        with tf.variable_scope(tf.get_variable_scope(),
                                               reuse=iter > 0):
                            probe_tensors, side_effects = self.build_step()

                    # copy probe data to array
                    for i, p in enumerate(probe_tensors):
                        probe_arrays[i] = probe_arrays[i].write(loop_i, p)

                    # need to make sure that any operators that could have side
                    # effects run each timestep, so we tie them to the loop
                    # increment. we also need to make sure that all the probe
                    # reads happen before those values get overwritten on the
                    # next timestep
                    with self.graph.control_dependencies(side_effects +
                                                         probe_tensors):
                        loop_i += 1

            base_vars = tuple(self.signals.bases.values())

            return step, stop, loop_i, probe_arrays, base_vars

        self.step_var = tf.placeholder(tf.int32, shape=(), name="step")
        self.stop_var = tf.placeholder(tf.int32, shape=(), name="stop")
        loop_i = tf.constant(0)

        probe_arrays = [
            tf.TensorArray(
                self.dtype, clear_after_read=True, size=0,
                dynamic_size=True)
            for _ in self.model.probes]

        # build simulation loop
        loop_vars = (
            self.step_var, self.stop_var, loop_i, probe_arrays,
            tuple(x[0]._ref() if isinstance(x[0], tf.Variable) else x[0]
                  for x in self.base_vars.values()) +
            tuple(x._ref() for x in self.signals.internal_vars.values()))

        loop_vars = tf.while_loop(
            loop_condition, loop_body, loop_vars=loop_vars,
            parallel_iterations=1, back_prop=not self.inference_only)

        self.steps_run = loop_vars[2]
        self.probe_arrays = OrderedDict()
        for p, a in zip(self.model.probes, loop_vars[3]):
            x = a.stack()

            if self.model.sig[p]["in"].minibatched:
                x = tf.transpose(x, np.roll(np.arange(x.get_shape().ndims), 1))
            else:
                x = tf.expand_dims(x, 0)

            self.probe_arrays[p] = x

    def build_inputs(self, progress):
        """
        Sets up the inputs in the model (which will be computed outside of
        TensorFlow and fed in each simulation block).

        Parameters
        ----------
        progress : :class:`.utils.ProgressBar`
            Progress bar for input construction
        """

        self.input_ph = {}
        for n in progress(self.invariant_inputs):
            if self.model.sig[n]["out"] in self.signals:
                # set up a placeholder input for this node
                self.input_ph[n] = tf.placeholder(
                    self.dtype, (None, n.size_out, self.minibatch_size),
                    name="%s_ph" % utils.sanitize_name(n))

    @with_self
    def build_optimizer(self, optimizer, objective):
        """
        Adds elements into the graph to execute the given optimizer.

        Parameters
        ----------
        optimizer : ``tf.train.Optimizer``
            Instance of a TensorFlow optimizer class
        objective : dict of {:class:`~nengo:nengo.Probe`: ``"mse"`` or \
                                                          callable or ``None``}
            The objective to be minimized for each probe. Passing
            ``"mse"`` will train with mean squared error. A custom function
            ``f(output, target) -> loss`` can be passed that consumes the
            actual output and target output for a probe in ``targets``
            and returns a ``tf.Tensor`` representing the scalar loss value for
            that Probe (loss will be summed across Probes).  ``None``
            indicates that the error gradient is being directly specified
            by the user.

        Returns
        -------
        ``tf.Tensor``
            Operator implementing the given optimizer update
        ``tf.Tensor`` or ``None``
            Operator for initializing variables created by the optimizer
            (``None`` if there is nothing to initialize, or if we're returning
            a previously built optimizer that should already be initialized)
        """

        loss = self.build_loss(objective)

        key = (optimizer, frozenset(objective.items()))

        try:
            # return the cached optimizer if it exists
            return self.optimizers[key], None
        except KeyError:
            pass

        agg_method = tf.AggregationMethod.DEFAULT

        # compute gradients wrt loss
        grads = []
        vars = tf.trainable_variables()
        with tf.variable_scope(tf.get_variable_scope()) as scope:
            if loss is not None:
                grads.append(tf.gradients(
                    loss, vars, aggregation_method=agg_method))

            # add in any gradients where the user directly specified the output
            # error grad
            for p, g in objective.items():
                if g is None:
                    grads.append(tf.gradients(
                        self.probe_arrays[p], vars, grad_ys=self.target_phs[p],
                        aggregation_method=agg_method))

            # get any new variables created by the gradient calculations
            new_vars = scope.get_collection("gradient_vars")

        if len(grads) == 1:
            grads = grads[0]
        else:
            grads = [tf.reduce_sum(gs, axis=0) for gs in zip(*grads)]

        with tf.variable_scope(optimizer.get_name()) as scope:
            # create optimizer operator
            opt_op = optimizer.apply_gradients(
                zip(grads, tf.trainable_variables()))

            # get any new variables created by the optimizer (so they
            # can be initialized)
            new_vars.extend(
                scope.get_collection(tf.GraphKeys.GLOBAL_VARIABLES))

        if len(new_vars) > 0:
            opt_slots_init = tf.variables_initializer(new_vars)
        else:
            opt_slots_init = None

        self.optimizers[key] = opt_op

        return opt_op, opt_slots_init

    @with_self
    def build_loss(self, objective):
        """
        Adds elements into the graph to compute the given objective.

        Parameters
        ----------
        objective : dict of {:class:`~nengo:nengo.Probe`: ``"mse"`` or \
                                                          callable or ``None``}
            The objective used to compute loss for each probe. Passing
            ``"mse"`` will use mean squared error. A custom function
            ``f(output, target) -> loss`` can be passed that consumes the
            actual output and target output for a probe in ``targets``
            and returns a ``tf.Tensor`` representing the scalar loss value for
            that Probe (loss will be summed across Probes).

        Returns
        -------
        ``tf.Tensor``
            Tensor representing the sum of the given objectives applied to
            target probes
        """

        key = frozenset(objective.items())

        try:
            # return the cached loss tensor if it exists
            return self.losses[key]
        except KeyError:
            pass

        loss = []
        for p, obj in objective.items():
            # create a placeholder for the target values
            if p not in self.target_phs:
                self.target_phs[p] = tf.placeholder(
                    self.dtype, (self.minibatch_size, None, p.size_in),
                    name="%s_ph" % utils.sanitize_name(p))

            # compute loss
            if obj == "mse":
                # note: nan targets converted to zero error
                target = tf.where(tf.is_nan(self.target_phs[p]),
                                  self.probe_arrays[p],
                                  self.target_phs[p])

                loss.append(tf.reduce_mean(
                    tf.square(target - self.probe_arrays[p])))
            elif callable(obj):
                loss.append(obj(self.probe_arrays[p], self.target_phs[p]))
            elif obj is None:
                # user is directly specifying error, not using objective
                continue
            else:
                raise NotImplementedError

        if len(loss) > 0:
            # sum loss across probes (note: this will also sum across
            # the output of `objective` if it doesn't return a scalar)
            loss = tf.reduce_sum(loss)
        else:
            loss = None

        self.losses[key] = loss

        return loss

    @with_self
    def build_post(self, sess, rng):
        """
        Executes post-build processes for operators (after the graph has
        been constructed and session/variables initialized).

        Note that unlike other build functions, this is called every time
        the simulator is reset.

        Parameters
        ----------
        sess : ``tf.Session``
            The TensorFlow session for the simulator
        rng : :class:`~numpy:numpy.random.RandomState`
            Seeded random number generator
        """

        # build input functions (we need to do this here, because in the case
        # of processes these functions depend on the rng, and need to be be
        # rebuilt on reset)
        self.input_funcs = {}
        for n, output in self.invariant_inputs.items():
            if isinstance(output, np.ndarray):
                self.input_funcs[n] = output
            elif isinstance(output, Process):
                self.input_funcs[n] = [
                    output.make_step(
                        (n.size_in,), (n.size_out,), self.dt,
                        output.get_rng(rng))
                    for _ in range(self.minibatch_size)]
            elif n.size_out > 0:
                self.input_funcs[n] = [
                    utils.align_func((n.size_out,), self.dtype)(output)]
            else:
                # a node with no inputs and no outputs, but it can still
                # have side effects
                self.input_funcs[n] = [output]

        # call build_post on all the op builders
        for ops, built_ops in self.op_builds.items():
            built_ops.build_post(ops, self.signals, sess, rng)

    @with_self
    def build_summaries(self, summaries):
        """
        Adds ops to collect summary data for the given objects.

        Parameters
        ----------
        summaries : list of dict or \
                            :class:`~nengo:nengo.Connection` or \
                            :class:`~nengo:nengo.Ensemble` or \
                            :class:`~nengo:nengo.ensemble.Neurons` or \
                            ``tf.Tensor``}
            List of objects for which we want to collect data.  Object can be a
            Connection (in which case data on weights will be collected),
            Ensemble (encoders), Neurons (biases), a dict of
            ``{probe: objective}`` that indicates a loss function that will
            be tracked, or a pre-built summary tensor.

        Returns
        -------
        ``tf.Tensor``
            Merged summary op for the given summaries
        """

        summary_ops = []
        with tf.device("/cpu:0"):
            for obj in summaries:
                if isinstance(obj, dict):
                    # overall loss
                    loss = self.build_loss(obj)
                    summary_ops.append(tf.summary.scalar(
                        "loss", loss, family="loss"))

                    if len(obj) > 1:
                        # get loss for each probe
                        inputs = tf.unstack(loss.op.inputs[0])
                        for p, t in zip(obj, inputs):
                            summary_ops.append(tf.summary.scalar(
                                utils.sanitize_name("Probe_%s_loss" % p.label),
                                t, family="loss"))
                elif isinstance(obj, (Ensemble, Neurons, Connection)):
                    if isinstance(obj, Ensemble):
                        param = "encoders"
                        name = "Ensemble_%s" % obj.label
                    elif isinstance(obj, Neurons):
                        param = "bias"
                        name = "Ensemble.neurons_%s" % obj.ensemble.label
                    elif isinstance(obj, Connection):
                        param = "weights"
                        name = "Connection_%s" % obj.label

                    summary_ops.append(tf.summary.histogram(
                        utils.sanitize_name("%s_%s" % (name, param)),
                        self.get_tensor(self.model.sig[obj][param])))
                elif isinstance(obj, tf.Tensor):
                    # we assume that obj is a summary op
                    summary_ops.append(obj)
                else:
                    raise SimulationError(
                        "Unknown summary object: %s" % obj)

            return tf.summary.merge(summary_ops)

    @with_self
    def get_tensor(self, sig):
        """
        Returns a Tensor corresponding to the given Signal.

        Parameters
        ----------
        sig : :class:`~nengo:nengo.builder.Signal`
            A signal in the model

        Returns
        -------
        ``tf.Tensor``
            Tensor containing the value of the given Signal
        """

        tensor_sig = self.signals[sig]

        base = self.base_vars[tensor_sig.key][0]

        if "while/" in tensor_sig.tf_indices.name:
            # rebuild tf indices outside the while loop
            tensor_sig._tf_indices = None

        return tf.gather(base, tensor_sig.tf_indices)

    def mark_signals(self):
        """
        Mark all the signals in ``self.model`` according to whether they
        represent trainable parameters of the model (parameters that can be
        optimized by deep learning methods).

        Trainable parameters include connection weights, ensemble encoders, and
        neuron biases.  Unless one of those signals is targeted by a Nengo
        learning rule (otherwise the learning rule update conflicts with the
        deep learning optimization).

        Users can manually specify whether signals are trainable or not using
        the config system (e.g.,
        ``net.config[nengo.Ensemble].trainable = False``)
        """

        def get_trainable(net_config, obj, network_trainable):
            """Looks up the current value of ``obj.trainable``."""

            if self.inference_only:
                return False

            try:
                if obj in net_config.params:
                    # priority #1: instance config
                    trainable = net_config[obj].trainable
                elif network_trainable is not 1:
                    # priority #2: network setting
                    trainable = network_trainable
                else:
                    # priority #3: class config
                    trainable = net_config[obj].trainable
            except (ConfigError, AttributeError):
                trainable = network_trainable

            # we return 1 if trainable isn't configured, since the default is
            # for everything to be trainable but we want to be able to
            # distinguish whether something was specifically set to be
            # trainable (True) or just defaulting to trainable (1)
            return 1 if trainable is None else trainable

        def mark_network(net_config, net, network_trainable):
            """Recursively marks the signals for objects within each
            subnetwork."""

            for subnet in net.networks:
                mark_network(net_config, subnet,
                             get_trainable(net_config, subnet,
                                           network_trainable))

            # encoders and biases are trainable
            for ens in net.ensembles:
                ens_trainable = get_trainable(net_config, ens,
                                              network_trainable)

                self.model.sig[ens]["encoders"].trainable = ens_trainable
                self.model.sig[ens]["encoders"].minibatched = False

                if not isinstance(ens.neuron_type, Direct):
                    neurons_trainable = get_trainable(net_config, ens.neurons,
                                                      network_trainable)
                    if neurons_trainable is 1:
                        neurons_trainable = ens_trainable

                    self.model.sig[ens.neurons]["bias"].trainable = (
                        neurons_trainable)
                    self.model.sig[ens.neurons]["bias"].minibatched = False

            # connection weights are trainable
            for conn in net.connections:
                # note: this doesn't include probe connections, since they
                # aren't added to the network
                self.model.sig[conn]["weights"].trainable = get_trainable(
                    net_config, conn, network_trainable)
                self.model.sig[conn]["weights"].minibatched = False

            # parameters can't be modified by an online Nengo learning rule
            # and offline training at the same time. (it is possible in
            # theory, but it complicates things a lot and is probably not a
            # common use case). we also make those signals minibatched
            # (they wouldn't be normally), because we want to be able to
            # learn independently in each minibatch
            for conn in net.connections:
                rule = conn.learning_rule
                if rule is not None:
                    if isinstance(rule, dict):
                        rule = list(rule.values())
                    elif not isinstance(rule, list):
                        rule = [rule]

                    for r in rule:
                        if r.modifies in ("weights", "decoders"):
                            obj = conn
                            attr = "weights"
                        elif r.modifies == "encoders":
                            obj = conn.post_obj
                            attr = "encoders"
                        else:
                            raise NotImplementedError

                        if self.model.sig[obj][attr].trainable is True:
                            warnings.warn(
                                "%s has a learning rule and is also set "
                                "to be trainable; this is likely to "
                                "produce strange training behaviour." %
                                obj)
                        else:
                            self.model.sig[obj][attr].trainable = False

                        self.model.sig[obj][attr].minibatched = True

        if self.model.toplevel is None:
            warnings.warn(
                "No top-level network in model; assuming no trainable "
                "parameters", UserWarning)
        else:
            net_config = self.model.toplevel.config
            mark_network(net_config, self.model.toplevel,
                         get_trainable(net_config, self.model.toplevel, 1))

            # the connections to connection probes are not trainable, but
            # also not minibatched
            probe_seeds = [self.model.seeds[p] for p in self.model.probes]
            for obj, seed in self.model.seeds.items():
                if isinstance(obj, Connection) and seed in probe_seeds:
                    self.model.sig[obj]["weights"].trainable = False
                    self.model.sig[obj]["weights"].minibatched = False

        # fill in defaults for all other signals
        # signals are not trainable by default, and views take on the
        # properties of their bases
        for op in self.model.operators:
            for sig in op.all_signals:
                if not hasattr(sig.base, "trainable"):
                    sig.base.trainable = False

                if not hasattr(sig.base, "minibatched"):
                    sig.base.minibatched = not sig.base.trainable

                if not hasattr(sig, "trainable"):
                    sig.trainable = sig.base.trainable

                if not hasattr(sig, "minibatched"):
                    sig.minibatched = sig.base.minibatched

    def create_signals(self, sigs):
        """
        Groups signal data together into larger arrays, and represent each
        individual signal as a slice into that array.

        Parameters
        ----------
        sigs : list of :class:`~nengo:nengo.builder.Signal`
            Base signals arranged into the order in which they should reside in
            memory (e.g., output from :func:`.graph_optimizer.order_signals`)
        """

        float_type = self.dtype.as_numpy_dtype
        base_arrays = OrderedDict()
        curr_keys = {}
        sig_idxs = {s: i for i, s in enumerate(sigs)}

        # find the non-overlapping partitions of the signals
        breaks = []
        diff = defaultdict(int)
        for ops in self.plan:
            # note: we don't include Resets, otherwise the big reset block
            # overrides most of the partitioning
            if not isinstance(ops[0], Reset):
                for i in range(len(ops[0].all_signals)):
                    op_sigs = [op.all_signals[i].base for op in ops]
                    idxs = [sig_idxs[s] for s in op_sigs]
                    diff[op_sigs[np.argmin(idxs)]] += 1
                    diff[op_sigs[np.argmax(idxs)]] -= 1

        # find the partition points in signal list
        open = 0
        for i, s in enumerate(sigs):
            if s in diff:
                open += diff[s]

            if open == 0:
                breaks += [i + 1]

        logging.debug("partitions")
        logging.debug("\n%s", "".join("|" if i in breaks else " "
                                      for i in range(len(sigs))))

        # create all the base signals
        for i, sig in enumerate(sigs):
            assert sig not in self.signals
            assert not sig.is_view

            if i in breaks:
                # start a new array for all current bases
                for k in curr_keys:
                    curr_keys[k] = object()

            # convert to appropriate dtype
            if np.issubdtype(sig.dtype, np.floating):
                dtype = float_type
            elif np.issubdtype(sig.dtype, np.integer):
                dtype = np.int32
            elif np.issubdtype(sig.dtype, np.bool_):
                dtype = sig.dtype
            else:
                raise NotImplementedError("Unsupported signal dtype")

            # resize scalars to length 1 vectors
            shape = sig.shape if sig.shape != () else (1,)

            # parameters of signal that affect the base array
            array_params = (dtype, shape[1:], sig.trainable, sig.minibatched)

            # key used to map signals to base arrays
            if array_params not in curr_keys:
                curr_keys[array_params] = object()
            key = curr_keys[array_params]

            initial_value = sig.initial_value.astype(dtype, copy=False)

            # broadcast scalars up to full size
            if initial_value.shape != shape:
                initial_value = np.resize(initial_value, shape)

            if sig.minibatched:
                # duplicate along minibatch dimension
                initial_value = np.tile(
                    initial_value[..., None],
                    tuple(1 for _ in shape) + (self.minibatch_size,))

            if key in base_arrays:
                base_arrays[key][0].append(initial_value)
                base_arrays[key][2] += shape[0]
            else:
                base_arrays[key] = [[initial_value], sig.trainable, shape[0]]

            n = base_arrays[key][-1]
            indices = np.arange(n - shape[0], n)

            tensor_sig = self.signals.get_tensor_signal(
                indices, key, dtype, shape, sig.minibatched, label=sig.name,
                signal=sig)

            logger.debug("created base signal")
            logger.debug(sig)
            logger.debug(tensor_sig)

        for key in base_arrays:
            arrs, t, _ = base_arrays[key]
            base_arrays[key] = (np.concatenate(arrs, axis=0), t)

        # add any signal views to the sig_map
        all_views = [sig for ops in self.plan for op in ops for sig in
                     op.all_signals if sig.is_view]
        for sig in all_views:
            if sig.size == sig.base.size:
                # reshape view
                self.signals[sig] = self.signals[sig.base].reshape(sig.shape)
            else:
                if sig.shape[1:] != sig.base.shape[1:]:
                    # TODO: support this?
                    raise NotImplementedError(
                        "Slicing on axes > 0 is not supported")

                # slice view
                assert np.all([x == 1 for x in sig.elemstrides[1:]])

                start = sig.elemoffset
                stride = sig.elemstrides[0]
                stop = start + sig.size * stride
                if stop < 0:
                    stop = None

                self.signals[sig] = self.signals[sig.base][slice(start, stop,
                                                                 stride)]

        # error checking
        for sig, tensor_sig in self.signals.items():
            # tensorsignal shapes should match signal shapes
            assert tensor_sig.shape == (sig.shape if sig.shape != () else (1,))

            # tensorsignal values should match signal values
            initial_value = sig.initial_value
            if sig.minibatched:
                initial_value = initial_value[..., None]

            assert np.allclose(
                base_arrays[tensor_sig.key][0][tensor_sig.indices],
                initial_value.astype(dtype))

        logger.debug("base arrays")
        logger.debug("\n".join([str((k, v.dtype, v.shape, trainable))
                                for k, (v, trainable) in base_arrays.items()]))

        self.base_arrays_init = base_arrays
