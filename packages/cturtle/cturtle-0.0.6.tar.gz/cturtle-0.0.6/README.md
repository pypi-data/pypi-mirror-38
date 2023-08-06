# A ctypes interface to the TURTLE library
( **T**opographic **U**tilities for t**R**ansporting par**T**icules over
  **L**ong rang**E**s )

## Description

This is yet an incomplete Python interface to the [TURTLE][TURTLE] library.
It is a pure Python package using ctypes. Note that it does not ship with
[TURTLE][TURTLE] which must be installed separately.

Currently only the `turtle_ecef` and `turtle_map` objects have been
encapsulated, as `cturtle.Ecef` and `cturtle.Map` Python classes. Feel free to
contribute with a [pull request][PR] if you need other [TURTLE][TURTLE] objects
to be integrated.

## Installation

From [PyPi][PyPi], e.g. using `pip`:
```bash
pip install --user cturtle
```
One can also do a manual install by copying the [cturtle.py][cturtle] source
file.

In addition the [TURTLE][TURTLE] library **must** be installed separately as a
shared library in a visible location, e.g. registered to `LD_LIBRARY_PATH`
on nix.

## License

The TURTLE library and the present Python interface are  under the **GNU
LGPLv3** license. See the provided [`LICENSE`][LICENSE] and
[`COPYING.LESSER`][COPYING] files.


[TURTLE]: https://niess.github.io/turtle-pages
[PR]: https://github.com/niess/turtle-python/pulls
[PyPi]: https://pypi.org/project/cturtle
[cturtle]: https://github.com/niess/turtle-python/blob/master/cturtle/cturtle.py
[LICENSE]: https://github.com/niess/turtle-python/blob/master/LICENSE
[COPYING]: https://github.com/niess/turtle-python/blob/master/COPYING.LESSER
