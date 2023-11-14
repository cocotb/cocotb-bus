***************
Testbench Tools
***************

Buses
=====

Buses are simply defined as collection of signals.
The :class:`.Bus` class will automatically bundle any group of signals together
that are named similar
to ``dut.<bus_name><separator><signal_name>``.
For instance,

.. code-block:: python3

        dut.stream_in_valid
        dut.stream_in_data

have a bus name of ``stream_in``, a separator of ``_``, and signal names of
``valid`` and ``data``. A list of signal names, or a dictionary mapping attribute
names to signal names is also passed into the :class:`.Bus` class.
Buses can have values driven onto them, be captured (returning a dictionary),
or sampled and stored into a similar object.

.. code-block:: python3

     stream_in_bus = Bus(dut, "stream_in", ["valid", "data"])  # '_' is the default separator


Driving Buses
=============

Examples and specific bus implementation bus drivers (AMBA, Avalon, XGMII, and
others) exist in the :class:`.Driver` class enabling a test to append
transactions to perform the serialization of transactions onto a physical
interface.
Here is an example using the :class:`~cocotb_bus.drivers.avalon.AvalonST` bus driver
in the ``endian_swapper`` example:

.. code-block:: python3

    from cocotb_bus.drivers.avalon import AvalonST as AvalonSTDriver


    class EndianSwapperTB(object):

        def __init__(self, dut, debug=False):
            self.dut = dut
            self.stream_in = AvalonSTDriver(dut, "stream_in", dut.clk)


    async def run_test(dut, data_in=None, config_coroutine=None, idle_inserter=None,
                       backpressure_inserter=None):

        cocotb.start_soon(Clock(dut.clk, (5000, "ns")).start())
        tb = EndianSwapperTB(dut)

        await tb.reset()
        dut.stream_out_ready.value = 1

        if idle_inserter is not None:
            tb.stream_in.set_valid_generator(idle_inserter())

        # Send in the packets
        for transaction in data_in():
            await tb.stream_in.send(transaction)


Monitoring Buses
================

For our testbenches to actually be useful, we have to monitor some of these
buses, and not just drive them. That's where the :class:`.Monitor` class
comes in, with pre-built monitors for Avalon and XGMII buses. The
Monitor class is a base class which you are expected to derive for your
particular purpose.

You must create a :func:`~cocotb_bus.monitors.Monitor._monitor_recv()` function
which is responsible for determining

1) at what points in time in the simulation to call the
   :func:`~cocotb_bus.monitors.Monitor._recv()` function,
   and

2) what transaction values to pass to be stored in the monitor's receiving queue.

Monitors are good for both outputs of the :term:`DUT` for
verification, and for the inputs of the DUT, to drive a test model of the DUT
to be compared to the actual DUT. For this purpose, input monitors will often
have a callback function passed that is a model. This model will often generate
expected transactions, which are then compared using the :class:`.Scoreboard`
class.

.. code-block:: python3

    class BitMonitor(Monitor):
        """Observe single input or output of DUT."""

        def __init__(self, name, signal, clock, callback=None, event=None):
            self.name = name
            self.signal = signal
            self.clock = clock
            Monitor.__init__(self, callback, event)

        async def _monitor_recv(self):
            clkedge = RisingEdge(self.clock)

            while True:
                # Capture signal at rising edge of clock
                await clkedge
                vec = self.signal.value
                self._recv(vec)


    def input_gen():
        """Generator for input data applied by BitDriver"""
        while True:
            yield random.randint(1,5), random.randint(1,5)


    class DFF_TB(object):
        def __init__(self, dut, init_val):

            self.dut = dut

            # Create input driver and output monitor
            self.input_drv = BitDriver(dut.d, dut.c, input_gen())
            self.output_mon = BitMonitor("output", dut.q, dut.c)

            # Create a scoreboard on the outputs
            self.expected_output = [ init_val ]

            # Reconstruct the input transactions from the pins
            # and send them to our 'model'
            self.input_mon = BitMonitor("input", dut.d, dut.c, callback=self.model)

        def model(self, transaction):
            """Model the DUT based on the input transaction."""
            # Do not append an output transaction for the last clock cycle of the
            # simulation, that is, after stop() has been called.
            if not self.stopped:
                self.expected_output.append(transaction)


Tracking Testbench Errors
=========================

The :class:`.Scoreboard` class is used to compare the actual outputs to
expected outputs. Monitors are added to the scoreboard for the actual outputs,
and the expected outputs can be either a simple list, or a function that
provides a transaction.

Here is some code from the ``dff`` example,
similar to the above,
with the scoreboard added.

.. code-block:: python3

    class DFF_TB(object):
        def __init__(self, dut, init_val):
            self.dut = dut

            # Create input driver and output monitor
            self.input_drv = BitDriver(dut.d, dut.c, input_gen())
            self.output_mon = BitMonitor("output", dut.q, dut.c)

            # Create a scoreboard on the outputs
            self.expected_output = [ init_val ]
            self.scoreboard = Scoreboard(dut)
            self.scoreboard.add_interface(self.output_mon, self.expected_output)

            # Reconstruct the input transactions from the pins
            # and send them to our 'model'
            self.input_mon = BitMonitor("input", dut.d, dut.c, callback=self.model)
