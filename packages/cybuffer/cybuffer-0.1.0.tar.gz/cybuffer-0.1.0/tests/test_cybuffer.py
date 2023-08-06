#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import array
import binascii
import contextlib
import mmap
import sys

import numpy
import pytest

from cybuffer import cybuffer


try:
    buffer
except NameError:
    buffer = memoryview


Py_UNICODE_SIZE = array.array('u').itemsize


def test_empty_constructor():
    with pytest.raises(TypeError):
        b = cybuffer()


def validate_against_memoryview(v, b, m, suboffsets=tuple()):
    # Test view properties' data relationships
    assert b.obj is v
    assert b.nbytes == len(m.tobytes())
    assert b.itemsize == (len(m.tobytes()) // len(v))
    assert b.ndim == m.ndim
    assert b.suboffsets == suboffsets
    assert b.shape == (len(v),)
    assert b.strides == (len(m.tobytes()) // len(v),)

    # Test Python 3+ properties
    if sys.version_info.major > 2:
        assert b.obj is m.obj
        assert b.c_contiguous == m.c_contiguous
        assert b.f_contiguous == m.f_contiguous
        assert b.contiguous == m.contiguous
        assert b.nbytes == m.nbytes

    # Test methods
    assert b.tobytes() == m.tobytes()
    if sys.version_info.major > 2:
        assert b.hex() == m.hex()
    else:
        assert b.hex() == binascii.hexlify(m)


@pytest.mark.parametrize("v", [
    b"abcdefghi",
    bytearray(b"abcdefghi"),
])
def test_bytes(v):
    # Initialize buffers
    b = cybuffer(v)
    m = memoryview(v)

    # Validate format
    assert b.format == m.format
    assert b.itemsize == m.itemsize

    # Validate contiguity
    assert b.c_contiguous
    assert b.f_contiguous
    assert b.contiguous

    # Validate permissions
    assert b.readonly == m.readonly

    # Test methods
    assert b.tolist() == m.tolist()

    validate_against_memoryview(v, b, m)


@pytest.mark.parametrize("f",
    ["b", "B", "h", "H", "i", "I", "l", "L", "q", "Q", "f", "d"]
)
def test_1d_arrays(f):
    # Skip some newer types
    if sys.version_info.major < 3 and f in "qQ":
        pytest.skip("Format `%s` not available on Python 2" % f)

    # Initialize buffers
    v = array.array(f, [0, 1, 2, 3, 4])
    b = cybuffer(v)
    m = memoryview(buffer(v))

    # Validate format
    assert b.format == v.typecode
    assert b.itemsize == v.itemsize

    # Validate contiguity
    assert b.c_contiguous
    assert b.f_contiguous
    assert b.contiguous

    # Validate permissions
    if isinstance(b, memoryview):
        assert b.readonly
    else:
        assert not b.readonly

    # Test methods
    assert b.tolist() == v.tolist()

    validate_against_memoryview(v, b, m)


@pytest.mark.parametrize("f, s", [
    ("c", b"Hello World!"),
    ("u", u"Hello World!"),
])
def test_1d_text_arrays(f, s):
    # Skip some newer types
    if sys.version_info.major > 2 and f is "c":
        pytest.skip("Format `%s` not available on Python 3" % f)

    # Initialize buffers
    v = array.array(f, s)
    b = cybuffer(v)
    m = memoryview(buffer(v))

    # Validate format
    assert b.itemsize == v.itemsize
    if f is "u" and Py_UNICODE_SIZE == 2:
        assert b.format == "H"
    elif f is "u" and Py_UNICODE_SIZE == 4:
        assert b.format == "I"
    elif f is "c":
        assert b.format == "B"

    # Validate contiguity
    assert b.c_contiguous
    assert b.f_contiguous
    assert b.contiguous

    # Validate permissions
    if isinstance(b, memoryview):
        assert b.readonly
    else:
        assert not b.readonly

    # Test methods
    assert b.tolist() == list(map(ord, v))

    validate_against_memoryview(v, b, m)


def test_mmap():
    with contextlib.closing(mmap.mmap(-1, 10, access=mmap.ACCESS_WRITE)) as v:
        # Initialize buffers
        b = cybuffer(v)
        m = memoryview(buffer(v))

        # Validate format
        assert b.format == m.format
        assert b.itemsize == m.itemsize

        # Validate contiguity
        assert b.c_contiguous
        assert b.f_contiguous
        assert b.contiguous

        # Validate permissions
        assert not b.readonly

        # Test methods
        assert b.tolist() == m.tolist()

        validate_against_memoryview(v, b, m)

        # Cleanup to close memory
        del b
        del m


@pytest.mark.parametrize("s",
    [(10,), (10, 11), (10, 11, 12)]
)
@pytest.mark.parametrize("o",
    ["C", "F"]
)
def test_nd_numpy_arrays(s, o):
    # Initialize buffers
    numpy.random.seed(42)
    a = numpy.random.random(s).astype(float, order=o)
    b = cybuffer(a)

    # Validate identity
    assert b.obj is a

    # Validate shape, size, etc.
    assert b.nbytes == a.nbytes
    assert b.ndim == a.ndim
    assert b.suboffsets == tuple()
    assert b.shape == a.shape
    assert b.strides == a.strides

    # Validate format
    assert b.format == a.dtype.char
    assert b.itemsize == a.itemsize

    # Validate contiguity
    assert b.c_contiguous == a.flags.c_contiguous
    assert b.f_contiguous == a.flags.f_contiguous
    assert b.contiguous == (a.flags.c_contiguous or a.flags.f_contiguous)

    # Validate permissions
    assert b.readonly != a.flags.writeable

    # Test methods
    assert b.tobytes() == a.tobytes()
    assert b.tolist() == a.tolist()
    if sys.version_info.major > 2:
        assert b.hex() == a.tobytes().hex()
    else:
        assert b.hex() == binascii.hexlify(a.tobytes())
