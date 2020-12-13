# Copyright cocotb contributors
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause


"""
    Collection of Ethernet Packet generators to use for testdata generation

    Most generators take the keyword argument "payload" which can be
    used to control the payload contents if required.  Defaults to random data.
"""
import random

from scapy.all import Ether, IP, UDP

# Supress SCAPY warning messages
import logging
logging.getLogger("scapy").setLevel(logging.ERROR)

from cocotb.decorators import public

from cocotb_bus.generators.byte import get_bytes, random_data

_default_payload = random_data


# UDP packet generators
@public
def udp_all_sizes(max_size=1500, payload=_default_payload()):
    """
    UDP packets of every supported size

    .. deprecated:: 1.4.1
    """
    header = Ether() / IP() / UDP()

    for size in range(0, max_size - len(header)):
        yield header / get_bytes(size, payload)


@public
def udp_random_sizes(npackets=100, payload=_default_payload()):
    """
    UDP packets with random sizes

    .. deprecated:: 1.4.1
    """
    header = Ether() / IP() / UDP()
    max_size = 1500 - len(header)

    for pkt in range(npackets):
        yield header / get_bytes(random.randint(0, max_size), payload)


# IPV4 generator
@public
def ipv4_small_packets(npackets=100, payload=_default_payload()):
    """
    Small (<100bytes payload) IPV4 packets

    .. deprecated:: 1.4.1
    """
    for pkt in range(npackets):
        yield Ether() / IP() / get_bytes(random.randint(0, 100), payload)
