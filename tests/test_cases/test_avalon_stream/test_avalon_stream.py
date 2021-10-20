"""Test to demonstrate functionality of the avalon basic streaming interface"""

import random
import struct
import warnings
import math

import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
from cocotb_bus.drivers import BitDriver
from cocotb_bus.drivers.avalon import AvalonST as AvalonSTDriver
from cocotb_bus.monitors.avalon import AvalonST as AvalonSTMonitor
from cocotb_bus.scoreboard import Scoreboard


def sine_wave(amplitude, w, offset=0):
    """
    Generates a sine wave that repeats forever
    Args:
        amplitude (int/float): peak deviation of the function from zero
        w (int/float): is the rate of change of the function argument
    Yields:
        floats that form a sine wave
    """
    twoPiF_DIV_sampleRate = math.pi * 2
    while True:
        for idx in (i / float(w) for i in range(int(w))):
            yield amplitude * math.sin(twoPiF_DIV_sampleRate * idx) + offset


def bit_toggler(gen_on, gen_off):
    """Combines two generators to provide cycles_on, cycles_off tuples
    Args:
        gen_on (generator): generator that yields number of cycles on
        gen_off (generator): generator that yields number of cycles off
    """
    for n_on, n_off in zip(gen_on, gen_off):
        yield int(abs(n_on)), int(abs(n_off))


def wave(on_ampl=30, on_freq=200, off_ampl=10, off_freq=100):
    """
    Drive a repeating sine_wave pattern
    TODO:
        Adjust args so we just specify a repeat duration and overall throughput
    """
    return bit_toggler(sine_wave(on_ampl, on_freq),
                       sine_wave(off_ampl, off_freq))


class AvalonSTTB(object):
    """Testbench for avalon basic stream"""

    def __init__(self, dut):
        self.dut = dut

        self.clkedge = RisingEdge(dut.clk)

        self.stream_in = AvalonSTDriver(self.dut, "asi", dut.clk)
        self.stream_out = AvalonSTMonitor(self.dut, "aso", dut.clk)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.scoreboard = Scoreboard(self.dut, fail_immediately=True)

        self.expected_output = []
        self.scoreboard.add_interface(self.stream_out, self.expected_output)

        self.backpressure = BitDriver(self.dut.aso_ready, self.dut.clk)

    async def initialise(self):
        self.dut.reset.value = 0
        cocotb.fork(Clock(self.dut.clk, 10).start())
        for _ in range(3):
            await self.clkedge
        self.dut.reset.value = 1
        await self.clkedge

    async def send_data(self, data):
        exp_data = struct.pack("B",data)
        self.expected_output.append(exp_data)
        await self.stream_in.send(data)


@cocotb.test()
async def test_avalon_stream(dut):
    """Test stream of avalon data"""

    tb = AvalonSTTB(dut)
    await tb.initialise()
    tb.backpressure.start(wave())

    for _ in range(20):
        data = random.randint(0, (2**7)-1)
        await tb.send_data(data)
        await tb.clkedge

    for _ in range(5):
        await tb.clkedge

    raise tb.scoreboard.result
