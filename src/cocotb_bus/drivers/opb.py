# Copyright cocotb contributors
# Copyright (c) 2015 Potential Ventures Ltd
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

"""
Drivers for On-chip Peripheral Bus.

NOTE: Currently we only support a very small subset of functionality.
"""

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from cocotb.binary import BinaryValue

from cocotb_bus.drivers import BusDriver


class OPBException(Exception):
    pass


class OPBMaster(BusDriver):
    """On-chip peripheral bus master."""
    _signals = ["xferAck", "errAck", "toutSup", "retry", "DBus_out", "select",
                "RNW", "BE", "ABus", "DBus_in"]
    _optional_signals = ["seqAddr"]
    _max_cycles = 16

    def __init__(self, entity, name, clock, **kwargs):
        BusDriver.__init__(self, entity, name, clock, **kwargs)
        self.bus.select.setimmediatevalue(0)
        self.log.debug("OPBMaster created")

    @cocotb.coroutine
    async def read(self, address: int, sync: bool = True) -> BinaryValue:
        """Issue a request to the bus and block until this comes back.

        Simulation time still progresses but syntactically it blocks.

        Args:
            address: The address to read from.
            sync: Wait for rising edge on clock initially.
                Defaults to True.

        Returns:
            The read data value.

        Raises:
            OPBException: If read took longer than 16 cycles.
        """
        await self._acquire_lock()

        # Apply values for next clock edge
        if sync:
            await RisingEdge(self.clock)
        self.bus.ABus.value = address
        self.bus.select.value = 1
        self.bus.RNW.value = 1
        self.bus.BE.value = 0xF

        count = 0
        while not int(self.bus.xferAck.value):
            await RisingEdge(self.clock)
            await ReadOnly()
            if int(self.bus.toutSup.value):
                count = 0
            else:
                count += 1
            if count >= self._max_cycles:
                raise OPBException("Read took longer than 16 cycles")
        data = int(self.bus.DBus_out.value)

        # Deassert read
        self.bus.select.value = 0
        self._release_lock()
        self.log.info("Read of address 0x%x returned 0x%08x" % (address, data))
        return data

    @cocotb.coroutine
    async def write(self, address: int, value: int, sync: bool = True) -> None:
        """Issue a write to the given address with the specified value.

        Args:
            address: The address to read from.
            value: The data value to write.
            sync: Wait for rising edge on clock initially.
                Defaults to True.

        Raises:
            OPBException: If write took longer than 16 cycles.
        """
        await self._acquire_lock()

        if sync:
            await RisingEdge(self.clock)
        self.bus.ABus.value = address
        self.bus.select.value = 1
        self.bus.RNW.value = 0
        self.bus.BE.value = 0xF
        self.bus.DBus_out.value = value

        count = 0
        while not int(self.bus.xferAck.value):
            await RisingEdge(self.clock)
            await ReadOnly()
            if int(self.bus.toutSup.value):
                count = 0
            else:
                count += 1
            if count >= self._max_cycles:
                raise OPBException("Write took longer than 16 cycles")

        self.bus.select.value = 0
        self._release_lock()
