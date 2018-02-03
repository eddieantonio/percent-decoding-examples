#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
from binascii import unhexlify


def suggested_method(text):
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
    def decode_triplet(match):
        hex_digits = match.group()[1:]
        return unhexlify(hex_digits)

    unencoded = text.encode('UTF-8')
    output = re.sub(b'%[0-9A-Fa-f]{2}', decode_triplet, unencoded)
    return output.decode('UTF-8')


decoders = [
    suggested_method,
    re_sub
]
