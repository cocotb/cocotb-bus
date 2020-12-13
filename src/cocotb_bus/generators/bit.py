# Copyright cocotb contributors
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

"""
    Collection of generators for creating bit signals.

    Typically we use a single bit to control backpressure or insert IDLE
    cycles onto a bus.

    These yield a tuple which is intended to be interpreted as a number of
    cycles ``(ON,OFF)``
"""
from cocotb.decorators import public

from cocotb_bus.generators import gaussian, sine_wave, repeat


def bit_toggler(gen_on, gen_off):
    """Combines two generators to provide cycles_on, cycles_off tuples

    Args:
        gen_on (generator): generator that yields number of cycles on
        gen_off (generator): generator that yields number of cycles off

    .. deprecated:: 1.4.1
    """
    for n_on, n_off in zip(gen_on, gen_off):
        yield int(abs(n_on)), int(abs(n_off))


@public
def intermittent_single_cycles(mean=10, sigma=None):
    """Generator to intermittently insert a single cycle pulse

    Args:
        mean (int, optional): Average number of cycles in between single cycle gaps
        sigma (int, optional): Standard deviation of gaps.  mean/4 if sigma is None

    .. deprecated:: 1.4.1
    """
    if sigma is None:
        sigma = mean / 4.0

    return bit_toggler(gaussian(mean, sigma), repeat(1))


@public
def random_50_percent(mean=10, sigma=None):
    """50% duty cycle with random width

    Args:
        mean (int, optional): Average number of cycles on/off
        sigma (int, optional): Standard deviation of gaps.  mean/4 if sigma is None

    .. deprecated:: 1.4.1
    """
    if sigma is None:
        sigma = mean / 4.0
    for duration in gaussian(mean, sigma):
        yield int(abs(duration)), int(abs(duration))


@public
def wave(on_ampl=30, on_freq=200, off_ampl=10, off_freq=100):
    """
    Drive a repeating sine_wave pattern

    TODO:
        Adjust args so we just specify a repeat duration and overall throughput

    .. deprecated:: 1.4.1
    """
    return bit_toggler(sine_wave(on_ampl, on_freq),
                       sine_wave(off_ampl, off_freq))
