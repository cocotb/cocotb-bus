# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause


from typing import Union

import cocotb

cocotb_2x_or_newer = cocotb.__version__.startswith("2")
if cocotb_2x_or_newer:
    from cocotb.types import Logic, LogicArray, Range

    BinaryType = LogicArray

    def create_binary(
        binstr: Union[int, str, bytes, LogicArray], bit_count: int, big_endian: bool
    ):
        if bit_count == 1:
            return Logic(binstr)

        if big_endian:
            range = Range(0, "to", bit_count - 1)
        else:
            range = Range(bit_count - 1, "downto", 0)

        if isinstance(binstr, bytes):
            if not big_endian:
                binstr = reversed(binstr)
            binstr = "".join([format(char, "08b") for char in binstr])

            if big_endian:
                binstr = binstr + "0" * (bit_count - len(binstr))
            else:
                binstr = "0" * (bit_count - len(binstr)) + binstr

        return LogicArray(binstr, range=range)

    def convert_binary_to_bytes(value: BinaryType, big_endian: bool):
        return value.to_bytes(byteorder="big" if big_endian else "little")

    def binary_slice(value: BinaryType, start: int, end: int):
        return value[value.range[start] : value.range[end]]

    def test_success():
        cocotb.pass_test()

else:
    from cocotb.binary import BinaryValue
    from cocotb.result import TestSuccess

    BinaryType = BinaryValue

    def create_binary(
        binstr: Union[int, str, bytes, BinaryValue], bit_count: int, big_endian: bool
    ):
        return BinaryValue(value=binstr, n_bits=bit_count, bigEndian=big_endian)

    def convert_binary_to_bytes(value: BinaryType, big_endian: bool):
        # Setting bigEndian does not affect initialization because value.binstr already is adjusted
        # to contain n_bits number of bits. Only access via buff is affected.
        value = BinaryValue(
            value=value.binstr, n_bits=value.n_bits, bigEndian=big_endian
        )
        return value.buff

    def binary_slice(value: BinaryType, start: int, end: int):
        # On 2.x the default slice direction is downto, whereas on 1.9.x it's to
        return value[start:end]

    def test_success():
        return TestSuccess()
