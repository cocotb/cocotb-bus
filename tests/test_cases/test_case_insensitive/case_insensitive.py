# Copyright cocotb contributors
# Copyright (c) 2022 benycze
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

import cocotb
import random
from cocotb.clock import Clock
from cocotb_bus.drivers import BusDriver
from cocotb_bus.monitors import BusMonitor
from cocotb.triggers import RisingEdge

class TestTransaction:

    def __init__(self, data, tmp):
        self.data = data
        self.tmp  = tmp

    def __eq__(self, o):
        if self.data != o.data:
            return False
        if self.tmp != o.tmp:
            return False
        return True
    
    def __str__(self):
        return "[data={}, tmp={}]".format(self.data, self.tmp)

class TestDriver(BusDriver):
    # Test is using lower cases for signal ports. It should be mapped
    # to uppercase port on entity
    _signals = ["data", "valid"]
    _optional_signals = ["tmp"]

    def __init__(self, entity, name, clock, **kwargs):
        BusDriver.__init__(self, entity, name, clock, **kwargs)
        # Setup initial values
        self.bus.valid.value = 0
        self.bus.data.value  = 0
        self.bus.tmp.value   = 0

    async def _driver_send(self, transaction, sync=True):
        clkedge = RisingEdge(self.clock)
        if sync:
            await clkedge

        self.log.info("Sending {}".format(transaction))
        self.bus.valid.value = 1
        self.bus.data.value  = transaction.data
        self.bus.tmp.value   = transaction.tmp

        await clkedge
        self.bus.valid.value = 0
        self.bus.data.value  = 0
        self.bus.tmp.value   = 0

class TestMonitor(BusMonitor):
    # Test is using lower cases for signal ports. It should be mapped
    # to uppercase port on entity
    _signals = ["data", "valid"]
    _optional_signals = ["tmp"]

    def __init__(self, entity, name, clock, **kwargs):
        BusMonitor.__init__(self, entity, name, clock, **kwargs)
        self.add_callback(self._get_result)
        self.expected = []

    async def _monitor_recv(self):
        clkedge = RisingEdge(self.clock)
        while True:
            await clkedge
            if not self.bus.valid.value:
                continue
            # Receive transaction and provide to _recv method
            tr = TestTransaction(int(self.bus.data), int(self.bus.tmp))
            self._recv(tr)

    def _get_result(self, transaction):
        self.log.info("Received transaction: {} ".format(str(transaction)))
        exp = self.expected.pop(0)
        assert exp == transaction, "Transaction {} and {} are not same.".format(str(exp), str(transaction))

    def add_expected(self, transaction):
        self.expected.append(transaction)

@cocotb.test()
async def test_case_insensitive(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.fork(clock.start())
    clkedge  = RisingEdge(dut.clk)
    in_data  = TestDriver(dut, "in", dut.clk)
    out_data = TestMonitor(dut, "in", dut.clk)
    # Generate random amount of transactions
    for i in range(0,20):
        tr = TestTransaction(random.randint(0, 1), random.randint(0, 1))
        out_data.add_expected(tr)
        await in_data.send(tr)
        await clkedge
    assert len(out_data) == 0, "Some transactions are still available"
