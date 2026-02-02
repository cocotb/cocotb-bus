# Copyright cocotb contributors
# Copyright (c) 2025 Benycze
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

import cocotb
import logging
import random
import time
from cocotb.clock import Clock
from cocotb_bus.drivers import BusDriver
from cocotb_bus.monitors import BusMonitor
from cocotb.triggers import RisingEdge

# from remote_pdb import RemotePdb; rpdb = RemotePdb("127.0.0.1", 4000)

class TestTransaction:
    CMD_READ        = 0
    CMD_WRITE       = 1
    STATUS_WR_DONE  = 0
    STATUS_WR_ERR   = 1

    def __init__(self, name, addr = None, data = None, cmd = None, status = None):
        """ Initialize the read/write transaction. This transaction is also used
        also in the case of transaction result.

        Param:
            - name - name of the transaction
            - addr - address to read/write
            - data - data to write/read
            - cmd  - read/write command
            - status - status to write
        """
        self.name   = name
        self.addr   = addr      if addr is not None else 0
        self.data   = data      if data is not None else 0
        self.cmd    = cmd       if cmd is not None else 0
        self.status = status    if status is not None else 0
        # Prepare logging
        self.log = logging.getLogger("cocotb.TestTransaction")
        self.log.info("Transaction created: %s", repr(self))

    def __repr__(self):
        """ Print the transaction info"""
        str_data  = [str(x) for x in [self.name, hex(self.addr), hex(self.data)]]
        str_data.append("CMD_READ" if self.cmd == TestTransaction.CMD_READ else "CMD_WRITE")
        str_data.append("STATUS_WR_DONE" if self.status == TestTransaction.STATUS_WR_DONE else "STATUS_WR_ERR")

        return "[NAME={}, ADDR={}, DATA={}, CMD={}, STATUS={}]".format(*str_data)

    def __eq__(self, o):
        if self.data is not None and self.data != o.data:
            return False
        if self.addr is not None and self.addr != o.addr:
            return False
        if self.cmd is not None and self.cmd != o.cmd:
            return False
        if self.status is not None and self.status != o.status:
            return False
        return True

class TestDriver(BusDriver):
    _signals = ["I_REG"]

    def __init__(self, entity, name, clock, **kwargs):
        BusDriver.__init__(self, entity, name, clock, **kwargs)
        # Initialize values
        self.bus.I_REG.DATA.value   = 0
        self.bus.I_REG.CMD.value    = 0
        self.bus.I_REG.ADDR.value   = 0
        self.bus.I_REG.VLD.value    = 0

    async def _driver_send(self, transaction, sync=True):
        assert (type(transaction) == TestTransaction), "TestTransaction class not detected!"
        # Synchronize on a clock cycle and assert data
        clkedge = RisingEdge(self.clock)
        await clkedge
        self.log.debug("Sending {}".format(transaction))
        self.bus.I_REG.DATA.value   = transaction.data
        self.bus.I_REG.CMD.value    = transaction.cmd
        self.bus.I_REG.ADDR.value   = transaction.addr
        self.bus.I_REG.VLD.value    = 1
        # Wait for one clock cycle and drop the valid down
        await clkedge
        self.bus.I_REG.DATA.value   = 0
        self.bus.I_REG.CMD.value    = 0
        self.bus.I_REG.ADDR.value   = 0
        self.bus.I_REG.VLD.value    = 0
        self.log.debug("Transaction sent!")

class TestMonitor(BusMonitor):

    _signals = ["O_REG"]

    def __init__(self, entity, name, clock, reset, **kwargs):
        BusMonitor.__init__(self, entity, name, clock, reset=reset, **kwargs)
        self.add_callback(self._get_result)
        self.expected = []

    async def _monitor_recv(self):
        while True:
            await RisingEdge(self.clock)
            if self.in_reset:
                continue

            if self.bus.O_REG.VLD.value == 0:
                continue

            # We have a valid request, create the transaction
            tr_name = "transaction_" + str(self.stats.received_transactions)
            tr = TestTransaction(tr_name,
                addr=None,
                data=self.bus.O_REG.DATA.value,
                cmd=None,
                status=self.bus.O_REG.WR_STATUS.value)
            self._recv(tr)

    def _get_result(self, transaction):
        assert (type(transaction) == TestTransaction), "TestTransaction class not detected!"
        exp = self.expected[0]
        self.log.info("Received transaction: {}".format(repr(transaction)))
        self.log.info("Expected transaction: {}".format(repr(exp)))
        assert (transaction == exp), f"Expected {exp} and received {transaction} transactions aren't same!"
        del self.expected[0]

    def add_expected(self, transaction):
        # rpdb.set_trace()
        self.log.debug("Adding expected transaction: {}".format(repr(transaction)))
        self.expected.append(transaction)

    def expected_is_empty(self):
        return len(self.expected) == 0


class TB(object):
    def __init__(self, dut):
        self.dut        = dut
        self.log        = logging.getLogger("cocotb.tb")
        # Driver, monitor, initial signal values and folks
        self.clock              = Clock(dut.CLK, 10, units="ns")
        self.dut.RESET.value    = 0
        # Create driver and monitor
        self.driver     = TestDriver(dut, None, dut.CLK)
        self.monitor    = TestMonitor(dut, None, dut.CLK, dut.RESET)

    async def _wait_for_start(self):
        """Wait for several clock cycles to start ..."""
        self.log.info("Some delay before start ...")
        for i in range(0,100):
            await RisingEdge(self.dut.CLK)

    async def _reset(self):
        """Run the reset of the design"""
        self.log.info("Reset in progress ...")
        self.dut.RESET.value = 1
        for i in range(1,10):
            self.log.info("Reset {} clock ...".format(str(i)))
            await RisingEdge(self.dut.CLK)
        self.dut.RESET.value = 0

    async def _end(self):
        """Wait several clock cycles to end the simulation"""
        self.log.info("Ending the testbench")
        for i in range(1,100):
            await RisingEdge(self.dut.CLK)
        self.log.info("Ending drivers & monitors")
        self.monitor.kill()
        self.driver.kill()

    async def _send_and_wait(self, tr):
        await self.driver.send(tr)
        await self.monitor.wait_for_recv()
        self.log.debug("Frame processed.")

    async def run(self):
        # Start clocks, run the reset
        cocotb.fork(self.clock.start())
        await self._reset()
        for it in range(0, 4000):
            self.log.info("Generating the transaction {} ...".format(it))
            # Generate random address and data
            data = random.randint(0, 2**32-1)
            addr = random.randint(0, 2**6-1)
            # Prepare write transaction and expected result
            wr_tr_name = "wr_" + str(it)
            wr_tr = TestTransaction(wr_tr_name,
                addr=addr,
                data=data,
                cmd=TestTransaction.CMD_WRITE,
                status=None)

            exp_wr_tr_name = "exp_wr_" + str(it)
            exp_wr_tr = TestTransaction(exp_wr_tr_name,
                addr=None,
                data=None,
                cmd=None,
                status=TestTransaction.STATUS_WR_DONE)

            self.monitor.add_expected(exp_wr_tr)
            await self._send_and_wait(wr_tr)

            # Prepare read transaction and expected result from the same address
            rd_tr_name = "rd_" + str(it)
            rd_tr = TestTransaction(rd_tr_name,
                addr=addr,
                data=None,
                cmd=TestTransaction.CMD_READ,
                status=None)

            exp_rd_tr_name = "exp_rd_" + str(it)
            exp_rd_tr = TestTransaction(exp_rd_tr_name,
                addr=None,
                data=data,
                cmd=None,
                status=None)

            self.monitor.add_expected(exp_rd_tr)
            await self._send_and_wait(rd_tr)
        # Kill monitor and driver thread
        assert (self.monitor.expected_is_empty()), "ERROR: Remaining transactions in monitor"
        await self._end()

@cocotb.test()
async def test_records(dut):
    cocotb.log.info("Starting the struct test.")
    tb = TB(dut)
    await tb.run()
    cocotb.log.info("Test done!")
