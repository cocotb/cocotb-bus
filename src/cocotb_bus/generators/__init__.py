# Copyright cocotb contributors
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

"""
    Set of general generic generators
"""
import math
import random
import itertools
import warnings

from cocotb.decorators import public


warnings.warn(
    "The contents of the cocotb.generators package will soon be removed.\n"
    "Most of the functionality can be replaced with utilities provided "
    "by other packages or the standard library.\n Alternatively, you can "
    "copy this package or individual functions into your project, if you "
    "follow cocotb's license agreement.",
    DeprecationWarning)


@public
def repeat(obj, nrepeat=None):
    """Generator to repeatedly yield the same object

    Args:
        obj (any): The object to yield
        nrepeat (int, optional): The number of times to repeatedly yield *obj*

    .. deprecated:: 1.4.1
    """
    if nrepeat is None:
        return itertools.repeat(obj)
    else:
        return itertools.repeat(obj, times=nrepeat)


@public
def combine(generators):
    """
    Generator for serially combining multiple generators together

    Args:
        generators (iterable): Generators to combine together

    .. deprecated:: 1.4.1
    """
    return itertools.chain.from_iterable(generators)


@public
def gaussian(mean, sigma):
    """
    Generate a guasian distribution indefinitely

    Args:
        mean (int/float): mean value

        sigma (int/float): Standard deviation

    .. deprecated:: 1.4.1
    """
    while True:
        yield random.gauss(mean, sigma)


@public
def sine_wave(amplitude, w, offset=0):
    """
    Generates a sine wave that repeats forever

    Args:
        amplitude (int/float): peak deviation of the function from zero

        w (int/float): is the rate of change of the function argument

    Yields:
        floats that form a sine wave

    .. deprecated:: 1.4.1
    """
    twoPiF_DIV_sampleRate = math.pi * 2
    while True:
        for idx in (i / float(w) for i in range(int(w))):
            yield amplitude*math.sin(twoPiF_DIV_sampleRate * idx) + offset


def get_generators(module):
    """Return an iterator which yields all the generators in a module

    Args:
        module (python module): The module to get the generators from

    .. deprecated:: 1.4.1
    """
    return (getattr(module, gen) for gen in module.__all__)
