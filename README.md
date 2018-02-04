Example percent-encoding decoders in Python
===========================================

A few different methods for performing percent-decoding in Python 3.

See `decoders.py`.

**NOTE**: These methods only work for *valid* percent-encoded strings.
The algorithms presented are **NOT** robust against invalid sequences.
There are a lot of UTF-8 sequences that are invalid, and should not be
decoded. As such, **DO NOT** use these algorithms in real code. Instead,
use what's builtin to your language, such as `from urllib.parse import
unquote`.

To run the tests
----------------

Install [tox](https://tox.readthedocs.io/en/latest/).

Then simply run `tox` in the root directory of this repository.

License
=======

Copyright © 2018 Eddie Antonio Santos. Licensed under the terms of
GPLv3. See LICENSE.
