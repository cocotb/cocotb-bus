# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause


from packaging.version import parse as parse_version
from typing import Optional, Union
import warnings

import cocotb

def TestFactory(*args, **kwargs):
    with warnings.catch_warnings():
        # TestFactory has been deprecated in v2.0 and there's no migration path in v1.x
        warnings.simplefilter("ignore")
        return cocotb.regression.TestFactory(*args, **kwargs)


cocotb_2x_or_newer = parse_version(cocotb.__version__) > parse_version("2.dev0")
if cocotb_2x_or_newer:
    from cocotb.types import LogicArray, Range
    BinaryType = LogicArray


    def set_event(event, data):
        event.data = data
        event.set()

    def coroutine(f):
        return f


    def create_binary(binstr: Union[int, str, bytes, LogicArray], bit_count: int, big_endian: bool):
        if big_endian:
            range=Range(0, 'to', bit_count - 1)
        else:
            range=Range(bit_count - 1, 'downto', 0)

        if isinstance(binstr, bytes):
            if not big_endian:
                binstr = reversed(binstr)
            binstr = "".join([format(char, "08b") for char in binstr])

            if big_endian:
                binstr = binstr + "0" * (bit_count - len(binstr))
            else:
                binstr = "0" * (bit_count - len(binstr)) + binstr

        return LogicArray(binstr, range=range)


    def create_binary_from_other(value: BinaryType, binstr: Union[int, str, bytes]):
        return LogicArray(value=binstr, range=value.range)


    def convert_binary_to_bytes(value: BinaryType, big_endian: bool):
        return value.to_bytes('big' if big_endian else 'little')


    def convert_binary_to_unsigned(value: Union[int, BinaryType]):
        if isinstance(value, int):
            return value
        return value.to_unsigned()


    def binary_slice(value: BinaryType, start: int, end: int):
        # On 2.x the default slice direction is downto, whereas on 1.9.x it's to
        # Additionally, in the case of BinaryValue slices always operate within 0..len(v) index
        # range regardless of how BinaryValue was acquired. In the case of LogicArray slices
        # operate on its range which doesn't necessarily start at zero. E.g. the following
        # returns top 8 bits: LogicArray(..., Range(31, 'downto', 0))[31:15][31:20][31:24]
        offset = min(value.range.left, value.range.right)
        start = len(value) - start - 1 + offset
        end = len(value) - end - 1 + offset
        return value[start:end]

else:
    from cocotb.binary import BinaryValue
    from cocotb.binary import _RESOLVE_TO_CHOICE

    coroutine = cocotb.coroutine
    BinaryType = BinaryValue


    def set_event(event, data):
        event.set(data)


    def create_binary(binstr: Union[int, str, bytes, BinaryValue], bit_count: int,
                      big_endian: bool):
        return BinaryValue(value=binstr, n_bits=bit_count, bigEndian=big_endian)


    def create_binary_from_other(value: BinaryType, binstr: Union[int, str, bytes]):
        return BinaryValue(value=binstr, n_bits=value.n_bits, bigEndian=value.big_endian)


    def convert_binary_to_bytes(value: BinaryType, big_endian: bool):
        # Setting bigEndian does not affect initialization because value.binstr already is adjusted
        # to contain n_bits number of bits. Only access via buff is affected.
        value = BinaryValue(value=value.binstr, n_bits=value.n_bits, bigEndian=big_endian)
        return value.buff


    def convert_binary_to_unsigned(value: Union[int, BinaryType]):
        # In 1.9.x code has more automatic conversions, therefore code does not consistently
        # apply .integer
        if isinstance(value, int):
            return value
        return value.integer


    def binary_slice(value: BinaryType, start: int, end: int):
        # On 2.x the default slice direction is downto, whereas on 1.9.x it's to
        return value[start:end]


def binary_is_resolvable(value: BinaryType):
    return value.is_resolvable
