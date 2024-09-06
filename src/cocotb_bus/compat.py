# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause


from packaging.version import parse as parse_version
import warnings

import cocotb

def TestFactory(*args, **kwargs):
    with warnings.catch_warnings():
        # TestFactory has been deprecated in v2.0 and there's no migration path in v1.x
        warnings.simplefilter("ignore")
        return cocotb.regression.TestFactory(*args, **kwargs)


def coroutine(f):
    if parse_version(cocotb.__version__) > parse_version("2.dev0"):
        return f

    return cocotb.coroutine(f)
