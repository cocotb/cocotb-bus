# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

try:
	from ._version import version as __version__  # noqa
except ModuleNotFoundError:
	__version__ = 'dev'
