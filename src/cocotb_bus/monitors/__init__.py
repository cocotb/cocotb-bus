# Copyright cocotb contributors
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

"""Class defining the standard interface for a monitor within a testbench.

The monitor is responsible for watching the pins of the DUT and recreating
the transactions.
"""

import logging
import warnings
from collections import deque

import cocotb
from cocotb.triggers import Event, First, Timer

from cocotb_bus.bus import Bus


class MonitorStatistics:
    """Wrapper class for storing Monitor statistics"""

    def __init__(self):
        self.received_transactions = 0


class Monitor:
    """Base class for Monitor objects.

    Monitors are passive 'listening' objects that monitor pins going in or out of a DUT.
    This class should not be used directly,
    but should be sub-classed and the internal :meth:`_monitor_recv` method should be overridden.
    This :meth:`_monitor_recv` method should capture some behavior of the pins, form a transaction,
    and pass this transaction to the internal :meth:`_recv` method.
    The :meth:`_monitor_recv` method is added to the cocotb scheduler during the ``__init__`` phase,
    so it should not be awaited anywhere.

    The primary use of a Monitor is as an interface for a :class:`~cocotb.scoreboard.Scoreboard`.

    Args:
        callback (callable): Callback to be called with each recovered transaction
            as the argument. If the callback isn't used, received transactions will
            be placed on a queue and the event used to notify any consumers.
        event (cocotb.triggers.Event): Event that will be called when a transaction
            is received through the internal :meth:`_recv` method.
            `Event.data` is set to the received transaction.
    """

    def __init__(self, callback=None, event=None):
        self._event = event
        if self._event is not None:
            self._event.data = (
                None  # FIXME: This attribute should be removed on next API break
            )
        self._wait_event = Event()
        self._wait_event_data = None
        self._recvQ = deque()
        self._callbacks = []
        self.stats = MonitorStatistics()

        # Sub-classes may already set up logging
        if not hasattr(self, "log"):
            self.log = logging.getLogger(
                "cocotb.monitor.%s" % (type(self).__qualname__)
            )

        if callback is not None:
            self.add_callback(callback)

        # Create an independent coroutine which can receive stuff
        self._thread = cocotb.start_soon(self._monitor_recv())

    def kill(self):
        """Kill monitor coroutine."""
        if self._thread:
            self._thread.kill()
            self._thread = None

    def __len__(self):
        return len(self._recvQ)

    def __getitem__(self, idx):
        return self._recvQ[idx]

    def add_callback(self, callback):
        """Add function as a callback.

        Args:
            callback (callable): The function to call back.
        """
        self.log.debug(
            "Adding callback of function %s to monitor", callback.__qualname__
        )
        self._callbacks.append(callback)

    async def wait_for_recv(self, timeout=None):
        """With *timeout*, :meth:`.wait` for transaction to arrive on monitor
        and return its data.

        Args:
            timeout: The timeout value for :class:`~.triggers.Timer`.
                Defaults to ``None``.

        Returns:
            Data of received transaction.
        """
        if timeout:
            t = Timer(timeout)
            fired = await First(self._wait_event.wait(), t)
            if fired is t:
                return None
        else:
            await self._wait_event.wait()

        return self._wait_event_data

    # this is not `async` so that we fail in `__init__` on subclasses without it
    def _monitor_recv(self):
        """Actual implementation of the receiver.

        Sub-classes should override this method to implement the actual receive
        routine and call :meth:`_recv` with the recovered transaction.
        """
        raise NotImplementedError(
            "Attempt to use base monitor class without "
            "providing a ``_monitor_recv`` method"
        )

    def _recv(self, transaction):
        """Common handling of a received transaction."""

        self.stats.received_transactions += 1

        # either callback based consumer
        for callback in self._callbacks:
            callback(transaction)

        # Or queued with a notification
        if not self._callbacks:
            self._recvQ.append(transaction)

        if self._event is not None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self._event.set(transaction)

        # If anyone was waiting then let them know
        if self._wait_event is not None:
            self._wait_event.set()
            self._wait_event_data = transaction
            self._wait_event.clear()


class BusMonitor(Monitor):
    """Wrapper providing common functionality for monitoring buses."""

    _signals = []
    _optional_signals = []

    def __init__(
        self,
        entity,
        name,
        clock,
        reset=None,
        reset_n=None,
        callback=None,
        event=None,
        **kwargs,
    ):
        self.log = logging.getLogger("cocotb.%s.%s" % (entity._name, name))
        self.entity = entity
        self.name = name
        self.clock = clock
        self.bus = Bus(
            self.entity,
            self.name,
            self._signals,
            optional_signals=self._optional_signals,
            **kwargs,
        )
        self._reset = reset
        self._reset_n = reset_n
        Monitor.__init__(self, callback=callback, event=event)

    @property
    def in_reset(self):
        """Boolean flag showing whether the bus is in reset state or not."""
        if self._reset_n is not None:
            return not bool(int(self._reset_n.value))
        if self._reset is not None:
            return bool(int(self._reset.value))
        return False

    def __str__(self):
        return "%s(%s)" % (type(self).__qualname__, self.name)
