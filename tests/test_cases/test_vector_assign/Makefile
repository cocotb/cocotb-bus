# Copyright cocotb contributors
# Copyright (c) 2022 benycze
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

TOPLEVEL_LANG := verilog
PWD=$(shell pwd)
TOPLEVEL := top
VERILOG_SOURCES = \
	$(PWD)/and_gate.v \
	$(PWD)/top.v

include $(shell cocotb-config --makefiles)/Makefile.sim

MODULE = top
