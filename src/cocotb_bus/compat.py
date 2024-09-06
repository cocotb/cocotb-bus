# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause


from packaging.version import parse as parse_version
import cocotb


def coroutine(f):
    if parse_version(cocotb.__version__) > parse_version("2.dev0"):
        return f

    return cocotb.coroutine(f)
