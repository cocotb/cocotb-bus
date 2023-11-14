*****************
Library Reference
*****************

.. spelling:word-list::
   AXIProtocolError
   BusDriver
   De
   Re
   ReadOnly
   args
   cbNextSimTime
   ing
   sim
   stdout
   un

Modules
=======

Bus
---

.. autoclass:: cocotb_bus.bus.Bus
    :members:
    :member-order: bysource

Driver
------

.. autoclass:: cocotb_bus.drivers.Driver
    :members:
    :member-order: bysource
    :private-members:

.. autoclass:: cocotb_bus.drivers.BitDriver
    :members:
    :member-order: bysource
    :show-inheritance:
    :private-members:

.. autoclass:: cocotb_bus.drivers.BusDriver
    :members:
    :member-order: bysource
    :show-inheritance:
    :private-members:

.. autoclass:: cocotb_bus.drivers.ValidatedBusDriver
    :members:
    :member-order: bysource
    :show-inheritance:
    :private-members:

Monitor
-------

.. autoclass:: cocotb_bus.monitors.Monitor
    :members:
    :member-order: bysource
    :private-members:

.. autoclass:: cocotb_bus.monitors.BusMonitor
    :members:
    :member-order: bysource
    :show-inheritance:
    :private-members:

Scoreboard
----------

.. automodule:: cocotb_bus.scoreboard
    :members:
    :member-order: bysource
    :show-inheritance:
    :synopsis: Class for scoreboards.


Implemented Testbench Structures
================================

Drivers
-------

AMBA
^^^^

Advanced Microcontroller Bus Architecture.

.. currentmodule:: cocotb_bus.drivers.amba

.. autoclass:: AXI4Master
    :members:
    :member-order: bysource

.. autoclass:: AXI4LiteMaster
    :members:
    :member-order: bysource

.. autoclass:: AXI4Slave
    :members:
    :member-order: bysource


Avalon
^^^^^^

.. currentmodule:: cocotb_bus.drivers.avalon

.. autoclass:: AvalonMM
    :members:
    :member-order: bysource
    :show-inheritance:

.. autoclass:: AvalonMaster
    :members:
    :member-order: bysource
    :show-inheritance:

.. autoclass:: AvalonMemory
    :members:
    :member-order: bysource
    :show-inheritance:

.. autoclass:: AvalonST
    :members:
    :member-order: bysource
    :show-inheritance:

.. autoclass:: AvalonSTPkts
    :members:
    :member-order: bysource
    :show-inheritance:


OPB
^^^

.. currentmodule:: cocotb_bus.drivers.opb

.. autoclass:: OPBMaster
    :members:
    :member-order: bysource
    :show-inheritance:


XGMII
^^^^^

.. currentmodule:: cocotb_bus.drivers.xgmii

.. autoclass:: XGMII
    :members:
    :member-order: bysource
    :show-inheritance:

Monitors
--------

Avalon
^^^^^^

.. currentmodule:: cocotb_bus.monitors.avalon

.. autoclass:: AvalonST
    :members:
    :member-order: bysource
    :show-inheritance:

.. autoclass:: AvalonSTPkts
    :members:
    :member-order: bysource
    :show-inheritance:

XGMII
^^^^^

.. autoclass:: cocotb_bus.monitors.xgmii.XGMII
    :members:
    :member-order: bysource
    :show-inheritance:
