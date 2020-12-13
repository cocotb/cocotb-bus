# Copyright cocotb contributors
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause


"""
    Collection of generators for creating byte streams.

    Note that on Python 3, individual bytes are represented with integers.
"""
import random
import itertools
from cocotb.decorators import public
from typing import Iterator


@public
def get_bytes(nbytes: int, generator: Iterator[int]) -> bytes:
    """
    Get nbytes from generator

    .. versionchanged:: 1.4.0
        This now returns :class:`bytes`, not :class:`str`.

    .. deprecated:: 1.4.1
    """
    return bytes(next(generator) for i in range(nbytes))


@public
def random_data() -> Iterator[int]:
    r"""
    Random bytes

    .. versionchanged:: 1.4.0
        This now returns integers, not single-character :class:`str`\ s.

    .. deprecated:: 1.4.1
    """
    while True:
        yield random.randrange(256)


@public
def incrementing_data(increment=1) -> Iterator[int]:
    r"""
    Incrementing bytes

    .. versionchanged:: 1.4.0
        This now returns integers, not single-character :class:`str`\ s.

    .. deprecated:: 1.4.1
    """
    val = 0
    while True:
        yield val
        val += increment
        val = val & 0xFF


@public
def repeating_bytes(pattern: bytes = b"\x00") -> Iterator[int]:
    """
    Repeat a pattern of bytes

    .. deprecated:: 1.4.1
    """
    return itertools.cycle(pattern)
