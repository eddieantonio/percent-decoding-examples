#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (C) 2018  Eddie Antonio Santos <easantos@ualberta.ca>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re
from binascii import unhexlify


def suggested_method(text):
    """
    The suggested algorithm for decoding percent-encoded UTF-8 strings.
    """
    unencoded = text.encode('UTF-8')
    output = b''
    while b'%' in unencoded:
        i = unencoded.find(b'%')
        output += unencoded[:i]
        unencoded = unencoded[i:]

        assert chr(unencoded[0]) == '%'
        byte = unhexlify(unencoded[1:3])
        output += byte
        unencoded = unencoded[3:]

    output += unencoded
    return output.decode('UTF-8')


def re_sub(text):
    """
    Using re.sub to invidually replace %XX triplets with bytes.
    """
    def decode_triplet(match):
        hex_digits = match.group()[1:]
        return unhexlify(hex_digits)

    unencoded = text.encode('UTF-8')
    output = re.sub(b'%[0-9A-Fa-f]{2}', decode_triplet, unencoded)
    return output.decode('UTF-8')


def re_sub_compact(text):
    """
    A more compact version of re_sub()
    """

    unencoded = text.encode('UTF-8')
    output = re.sub(b'%([0-9A-Fa-f]{2})',
                    lambda m: unhexlify(m.group(1)),
                    unencoded)
    return output.decode('UTF-8')


decoders = [
    suggested_method,
    re_sub,
    re_sub_compact
]
