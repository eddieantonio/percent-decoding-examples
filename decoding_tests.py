#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from urllib.parse import quote

import pytest
from hypothesis import given
from hypothesis.strategies import text

from decoders import decoders


@pytest.mark.parametrize("decode", decoders)
@given(s=text())
def test_full_unicode_range(s, decode):
    assert s == decode(quote(s))
