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
    undecoded = text.encode('UTF-8')
    output = b''
    while b'%' in undecoded:
        i = undecoded.index(b'%')
        output += undecoded[:i]
        undecoded = undecoded[i:]

        assert chr(undecoded[0]) == '%'
        byte = unhexlify(undecoded[1:3])
        output += byte
        undecoded = undecoded[3:]

    output += undecoded
    return output.decode('UTF-8')


def re_sub(text):
    """
    Using re.sub to invidually replace %XX triplets with bytes.
    """
    def decode_triplet(match):
        hex_digits = match.group()[1:]
        return unhexlify(hex_digits)

    undecoded = text.encode('UTF-8')
    output = re.sub(b'%[0-9A-Fa-f]{2}', decode_triplet, undecoded)
    return output.decode('UTF-8')


def re_sub_compact(text):
    """
    A more compact version of re_sub()
    """

    undecoded = text.encode('UTF-8')
    output = re.sub(b'%([0-9A-Fa-f]{2})',
                    lambda m: unhexlify(m.group(1)),
                    undecoded)
    return output.decode('UTF-8')


def partial_utf_8_decoder(undecoded):
    """
    Decodes by finding the first percent-encoded string and determining how
    many more percent-encoded bytes follow it in UTF-8 encoding.
    By Unicode terminology, when a percent is found, this algorithm proceeds
    to decode the "minimal well-formed code unit subsequence", i.e., the
    minimum number of bytes (or %xx) that will form one valid UTF-8 character.
    """

    def decode_triplet(text):
        """
        Helper that decodes the %xx triplet at the beginning of `text`.
        Returns one byte from three characters in `text`.
        """
        assert text.startswith('%')
        return bytes.fromhex(text[1:3])

    output = ""
    while '%' in undecoded:
        i = undecoded.find('%')

        # Everything up to i is not percent-encoded.
        output += undecoded[:i]
        undecoded = undecoded[i:]

        # In order to figure out how many bytes are in this character,
        # we have to judge it from the first byte of the sequence.
        first_byte = decode_triplet(undecoded)

        # Length of UTF-8 sequence based on first byte.
        #
        # Bits      | Range   | Length
        # --------- | ------- | -------
        # 0xxx xxxx | %00-%7f | 1 byte   (equivalent to ASCII)
        # 110x xxxx | %C0-%DF | 2 bytes
        # 1110 xxxx | %E0-%EF | 3 bytes
        # 1111 0xxx | %F0-%F7 | 4 bytes

        if first_byte <= b'\x7F':
            # An ASCII byte.
            output += first_byte.decode('ASCII')
            # Take this triple out of the sequence
            undecoded = undecoded[3:]
        elif b'\xC0' <= first_byte <= b'\xDF':
            # Two byte sequence.
            output += (
                first_byte +
                decode_triplet(undecoded[3:])
            ).decode('UTF-8')
            undecoded = undecoded[6:]
        elif b'\xE0' <= first_byte <= b'\xEF':
            # Three byte sequence.
            output += (
                first_byte +
                decode_triplet(undecoded[3:]) +
                decode_triplet(undecoded[6:])
            ).decode('UTF-8')
            undecoded = undecoded[9:]
        elif b'\xF0' <= first_byte <= b'\xF7':
            # Four byte sequence.
            output += (
                first_byte +
                decode_triplet(undecoded[3:]) +
                decode_triplet(undecoded[6:]) +
                decode_triplet(undecoded[9:])
            ).decode('UTF-8')
            undecoded = undecoded[12:]
        else:
            raise ValueError(first_byte)
    output += undecoded
    return output


decoders = [
    suggested_method,
    re_sub,
    re_sub_compact,
    partial_utf_8_decoder
]
