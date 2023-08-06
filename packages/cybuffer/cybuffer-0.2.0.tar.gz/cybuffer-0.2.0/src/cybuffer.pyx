include "config.pxi"

cimport cybuffer

cimport cython
cimport cython.view

from cython.view cimport memoryview as cvmemoryview

cimport cpython.buffer
cimport cpython.bytes
cimport cpython.list
cimport cpython.mem
cimport cpython.tuple

from cpython.array cimport array
from cpython.buffer cimport Py_buffer
from cpython.buffer cimport (
    PyBUF_FORMAT, PyBUF_WRITABLE,
    PyBUF_ND, PyBUF_STRIDES, PyBUF_INDIRECT,
    PyBUF_C_CONTIGUOUS, PyBUF_F_CONTIGUOUS, PyBUF_ANY_CONTIGUOUS,
    PyBUF_FULL_RO
)
from cpython.mem cimport PyMem_Malloc, PyMem_Free

from array import array
from struct import Struct

IF PY2K:
    from binascii import hexlify

include "version.pxi"


cdef extern from "Python.h":
    object PyMemoryView_FromObject(object obj)


cdef extern from *:
    """
    #define UINT8_TC "B"
    #define UINT16_TC "H"
    #define UINT32_TC "I"

    #define PyList_SET_ITEM_INC(l, i, o)  \
            Py_INCREF(o); PyList_SET_ITEM(l, i, o)
    #define PyTuple_SET_ITEM_INC(l, i, o)  \
            Py_INCREF(o); PyTuple_SET_ITEM(l, i, o)
    """

    char* UINT8_TC
    char* UINT16_TC
    char* UINT32_TC

    void PyList_SET_ITEM_INC(object, Py_ssize_t, object)
    void PyTuple_SET_ITEM_INC(object, Py_ssize_t, object)


IF PY2K:
    cimport cpython.oldbuffer
    from cpython.oldbuffer cimport (
        PyBuffer_FromReadWriteObject, PyBuffer_FromObject
    )


    cdef extern from "Python.h":
        int PyObject_AsWriteBuffer(object obj,
                                   void **buffer,
                                   Py_ssize_t *buffer_len) except -1


    cpdef getbuffer(obj, Py_ssize_t offset=0, Py_ssize_t size=-1):
        cdef void* buf_ptr
        cdef Py_ssize_t buf_len

        try:
            PyObject_AsWriteBuffer(obj, &buf_ptr, &buf_len)
        except TypeError:
            return PyBuffer_FromObject(obj, offset, size)
        else:
            return PyBuffer_FromReadWriteObject(obj, offset, size)


cdef tuple pointer_to_tuple(int n, Py_ssize_t* p):
    cdef int i
    cdef object p_i
    cdef tuple result

    result = cpython.tuple.PyTuple_New(n)
    for i in range(n):
        p_i = long(p[i])
        PyTuple_SET_ITEM_INC(result, i, p_i)

    return result


@cython.boundscheck(False)
@cython.infer_types(True)
@cython.initializedcheck(False)
@cython.nonecheck(False)
@cython.wraparound(False)
cdef list pointer_to_nested_list(int n,
                                 Py_ssize_t* shape,
                                 Py_ssize_t* strides,
                                 Py_ssize_t* suboffsets,
                                 object unpack,
                                 Py_ssize_t itemsize,
                                 const char* d):
    cdef list r
    cdef object r_i
    cdef Py_ssize_t i, l, s, so

    l = shape[0]
    s = strides[0]
    so = -1 if suboffsets is NULL else suboffsets[0]
    r = cpython.list.PyList_New(l)
    if n > 1:
        n -= 1
        shape += 1
        strides += 1
        if suboffsets is not NULL:
            suboffsets += 1
        for i in range(l):
            r_i = pointer_to_nested_list(
                n, shape, strides, suboffsets, unpack, itemsize,
                d if so < 0 else (<const char**>d)[0] + so
            )
            PyList_SET_ITEM_INC(r, i, r_i)
            d += s
    else:
        for i in range(l):
            r_i = (d if so < 0 else (<const char**>d)[0] + so)[:itemsize]
            r_i = unpack(r_i)[0]
            PyList_SET_ITEM_INC(r, i, r_i)
            d += s

    return r


cdef class cybuffer(object):
    """
    Constructs a ``memoryview`` from the buffer exposed by ``data``

    Attempts to use the (new) buffer interface. Falls back to the
    old buffer interface on Python 2 if that does not work. Smooths
    over some type handling issues of builtin types as needed.
    """


    @cython.cdivision(True)
    def __cinit__(self, data):
        """
        Take a memoryview of the data and hold onto it.
        """

        self.obj = data

        # Fallback to old buffer protocol on Python 2 if necessary
        if PY2K and not cpython.buffer.PyObject_CheckBuffer(data):
            data = getbuffer(data)

        # Fill out our buffer based on the data
        cpython.buffer.PyObject_GetBuffer(data, &self._buf, PyBUF_FULL_RO)

        # Allocate and/or initialize metadata for casting
        self._format = self._buf.format
        self.itemsize = self._buf.itemsize
        self._shape = self._buf.shape
        self._strides = self._buf.strides

        # Figure out whether the data is contiguous
        self.c_contiguous = cpython.buffer.PyBuffer_IsContiguous(
            &self._buf, b'C'
        )
        self.f_contiguous = cpython.buffer.PyBuffer_IsContiguous(
            &self._buf, b'F'
        )
        self.contiguous = self.c_contiguous or self.f_contiguous

        # Workaround some special cases with the builtin array
        IF PY2K or PY3K:
            cdef char fmt
        if (PY2K or PY3K) and isinstance(self.obj, array):
            # Correct itemsize and format on Python 2
            if PY2K:
                self.itemsize = self.obj.itemsize
                self._format = self.obj.typecode

            # Recast text formats
            fmt = self._format[0]
            if PY2K and fmt == 'c':
                self._format = UINT8_TC
            elif fmt == 'u' or fmt == 'w':
                if self.itemsize == 2:
                    self._format = UINT16_TC
                elif self.itemsize == 4:
                    self._format = UINT32_TC

            # Adjust shape and strides based on casting
            if PY2K and self.itemsize != 1:
                self._shape = <Py_ssize_t*>PyMem_Malloc(sizeof(Py_ssize_t))
                self._strides = <Py_ssize_t*>PyMem_Malloc(sizeof(Py_ssize_t))

                self._shape[0] = self._buf.shape[0] // self.itemsize
                self._strides[0] = self._buf.strides[0] * self.itemsize


    def __dealloc__(self):
        if PY2K:
            if self._shape != self._buf.shape:
                PyMem_Free(self._shape)
            if self._strides != self._buf.strides:
                PyMem_Free(self._strides)

        cpython.buffer.PyBuffer_Release(&self._buf)

        self._format = NULL
        self._shape = NULL
        self._strides = NULL


    @property
    def readonly(self):
        return self._buf.readonly


    @property
    def format(self):
        cdef bytes _format = self._format

        if PY2K:
            return _format
        else:
            return _format.decode("ascii")


    @property
    def ndim(self):
        return self._buf.ndim


    @property
    def nbytes(self):
        return self._buf.len


    @property
    def shape(self):
        return pointer_to_tuple(self._buf.ndim, self._shape)


    @property
    def strides(self):
        return pointer_to_tuple(self._buf.ndim, self._strides)


    @property
    def suboffsets(self):
        cdef tuple r
        if self._buf.suboffsets is NULL:
            r = tuple()
        else:
            r = pointer_to_tuple(self._buf.ndim, self._buf.suboffsets)
        return r


    def __len__(self):
        return self._shape[0]


    def __getitem__(self, key):
        cdef object r
        cdef cvmemoryview mv = cvmemoryview(self, PyBUF_FULL_RO)

        r = mv[key]
        if isinstance(r, cvmemoryview):
            r = cybuffer(r)

        return r


    def __setitem__(self, key, value):
        cdef cvmemoryview mv = cvmemoryview(self, PyBUF_FULL_RO)
        mv[key] = value


    cpdef str hex(self):
        cdef object d
        cdef str s

        if self.c_contiguous:
            d = self
        else:
            d = self.tobytes()

        if PY2K:
            s = hexlify(d)
        else:
            s = PyMemoryView_FromObject(d).hex()

        return s


    cpdef bytes tobytes(self):
        cdef bytes r
        cdef char* s

        r = cpython.bytes.PyBytes_FromStringAndSize(NULL, self._buf.len)
        s = cpython.bytes.PyBytes_AS_STRING(r)

        cpython.buffer.PyBuffer_ToContiguous(
            s, &self._buf, self._buf.len, b'C'
        )

        return r


    cpdef list tolist(self):
        return pointer_to_nested_list(
            self._buf.ndim, self._shape, self._strides, self._buf.suboffsets,
            Struct(self._format).unpack, self.itemsize,
            <const char*>self._buf.buf
        )


    def __getbuffer__(self, Py_buffer* buf, int flags):
        if (flags & PyBUF_ANY_CONTIGUOUS) == PyBUF_ANY_CONTIGUOUS:
            if not self.contiguous:
                raise BufferError("data is not contiguous")
        if (flags & PyBUF_C_CONTIGUOUS) == PyBUF_C_CONTIGUOUS:
            if not self.c_contiguous:
                raise BufferError("data is not C contiguous")
        if (flags & PyBUF_F_CONTIGUOUS) == PyBUF_F_CONTIGUOUS:
            if not self.f_contiguous:
                raise BufferError("data is not F contiguous")

        if (flags & PyBUF_WRITABLE) == PyBUF_WRITABLE:
            if self._buf.readonly:
                raise BufferError("data is readonly")

        buf.buf = self._buf.buf
        buf.obj = self
        buf.len = self._buf.len
        buf.readonly = self._buf.readonly
        buf.itemsize = self.itemsize
        buf.ndim = self._buf.ndim
        buf.internal = <void*>NULL

        if (flags & PyBUF_FORMAT) == PyBUF_FORMAT:
            buf.format = self._format
        else:
            buf.format = NULL

        if (flags & PyBUF_ND) == PyBUF_ND:
            buf.shape = self._shape
        else:
            buf.shape = NULL

        if (flags & PyBUF_STRIDES) == PyBUF_STRIDES:
            buf.strides = self._strides
        else:
            buf.strides = NULL

        if (flags & PyBUF_INDIRECT) == PyBUF_INDIRECT:
            buf.suboffsets = self._buf.suboffsets
        else:
            buf.suboffsets = NULL


    def __releasebuffer__(self, Py_buffer* buf):
        pass


    def __getreadbuffer__(self, Py_ssize_t i, void** p):
        if i != 0:
            raise ValueError("Accessing non-existent segment")
        if not self.contiguous:
            raise ValueError("Data is not contiguous")

        p[0] = self._buf.buf

        return self._buf.len


    def __getwritebuffer__(self, Py_ssize_t i, void** p):
        if i != 0:
            raise ValueError("Accessing non-existent segment")
        if not self.contiguous:
            raise ValueError("Data is not contiguous")
        if self._buf.readonly:
            raise TypeError("Buffer is read-only")

        p[0] = self._buf.buf

        return self._buf.len


    def __getsegcount__(self, Py_ssize_t* p):
        return 1


    def __getcharbuffer__(self, Py_ssize_t i, char** p):
        if i != 0:
            raise ValueError("Accessing non-existent segment")
        if not self.contiguous:
            raise ValueError("Data is not contiguous")

        p[0] = <char*>self._buf.buf

        return self._buf.len
