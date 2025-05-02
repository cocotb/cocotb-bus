# Copyright (c) 2013, 2018 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Potential Ventures Ltd,
#       SolarFlare Communications Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL POTENTIAL VENTURES LTD BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
A set of tests that demonstrate cocotb functionality

Also used as regression test of cocotb capabilities
"""

import logging

import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
from cocotb_bus.drivers.avalon import AvalonST, AvalonSTPkts, AvalonMaster
from cocotb_bus.monitors.avalon import AvalonST as AvalonSTMonitor
from cocotb_bus.monitors.avalon import AvalonSTPkts as AvalonSTPktsMonitor

if cocotb.simulator.is_running():
    data_bits = int(cocotb.top.DataWidth.value)
    address_bits = int(cocotb.top.AddrWidth.value)


class AvlSTFeedback(object):
    """class to test avalon interfaces"""

    def __init__(self, dut):
        self.dut = dut
        self.st_data = list(range(10))

        self.st_out_if = AvalonST(
            entity=self.dut.i_feedback_if,
            name=None,
            clock=dut.clk,
            config={
                "firstSymbolInHighOrderBits": False,
                "dataBitsPerSymbol": data_bits,
            },
        )

        self.st_in_if = AvalonSTMonitor(
            entity=self.dut.o_feedback_if,
            name=None,
            clock=dut.clk,
            config={
                "firstSymbolInHighOrderBits": False,
                "dataBitsPerSymbol": data_bits,
            },
            callback=self.check_st_output,
        )

    def check_st_output(self, transaction):
        assert int.from_bytes(transaction, "little") == self.st_data.pop(0), (
            "Mismatch between written and read data in Avalon stream port."
        )

    async def start(self):
        for datum in self.st_data:
            await RisingEdge(self.dut.clk)
            self.st_out_if.append(datum)


class AvlSTPktFeedback(object):
    """class to test avalon interfaces"""

    def __init__(self, dut):
        self.dut = dut
        self.st_pkt_data = b"".join(
            [i.to_bytes(data_bits // 8, "little") for i in range(10)]
        )

        self.st_pkt_out_if = AvalonSTPkts(
            entity=self.dut.i_feedback_if,
            name=None,
            clock=dut.clk,
            config={
                "firstSymbolInHighOrderBits": False,
                "dataBitsPerSymbol": data_bits,
            },
        )

        self.st_pkt_in_if = AvalonSTPktsMonitor(
            entity=self.dut.o_feedback_if,
            name=None,
            clock=dut.clk,
            config={
                "firstSymbolInHighOrderBits": False,
                "dataBitsPerSymbol": data_bits,
            },
            callback=self.check_st_pkt_output,
        )

    def check_st_pkt_output(self, transaction):
        assert transaction == self.st_pkt_data, (
            "Mismatch between written and read data in Avalon stream packetized port."
        )

    async def start(self):
        self.st_pkt_out_if.append(self.st_pkt_data)


class AvlMMRead(object):
    """class to test avalon interfaces"""

    def __init__(self, dut):
        self.dut = dut

        self.mm_master = AvalonMaster(
            entity=self.dut.mem_port_if,
            name=None,
            clock=self.dut.clk,
        )

    async def start(self):
        await self.test_avl_mem()

    async def test_avl_mem(self):
        for i in range(10):
            await self.mm_master.write(address=i, value=i)
            await RisingEdge(self.dut.clk)
        for i in range(10):
            data = await self.mm_master.read(address=i)
            assert data == i, (
                "Mismatch between written and read data in Avalon MM master."
            )
            await RisingEdge(self.dut.clk)


@cocotb.test()
async def test_avalon_st_feedback(dut):
    dut._log.setLevel(logging.INFO)
    # initialize memory control signals to 0
    dut.mem_port_if.read.value = 0
    dut.mem_port_if.write.value = 0

    # create testbench object
    tb = AvlSTFeedback(dut)

    # start clock
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    await tb.start()
    dut.o_feedback_if.ready.value = 1
    await Timer(1, "us")


@cocotb.test()
async def test_avalon_st_pkt_feedback(dut):
    dut._log.setLevel(logging.INFO)
    # initialize memory control signals to 0
    dut.mem_port_if.read.value = 0
    dut.mem_port_if.write.value = 0

    # create testbench object
    tb = AvlSTPktFeedback(dut)

    # start clock
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    await tb.start()
    dut.o_feedback_if.ready.value = 1
    await Timer(1, "us")


@cocotb.test()
async def test_avalon_mm_read(dut):
    dut._log.setLevel(logging.INFO)
    # initialize memory control signals to 0
    dut.mem_port_if.read.value = 0
    dut.mem_port_if.write.value = 0

    # create testbench object
    tb = AvlMMRead(dut)

    # start clock
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    await tb.start()
    await Timer(1, "us")
