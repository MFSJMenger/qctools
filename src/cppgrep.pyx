# distutils: language = c++

from libcpp.string cimport string
from libcpp.vector cimport vector

cdef extern from "filehandler.hpp":
    cdef cppclass File:
        File(const string filename) except +
        File(const int fileno, const int pos) except +
    cdef cppclass FileIterator:
        FileIterator(const string filename) except +
        FileIterator(const int fileno, const int pos) except +
        int grep(string key, size_t ilen, size_t ishift, vector[string]& vec)
        int seek(const int offset) 
        int tell()


class FileContextManager(object):

    def __init__(self, iterator):
        self.iterator = iterator

    def __enter__(self):
        # update cpp iterator
        self.iterator.cpp_iterator.seek(self.iterator.tell)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # update normal iterator
        self.iterator.seek(self.iterator.cpp_iterator.tell())



cdef class PyFileIterator:

    # python wrapper for FileIterator 

    cdef FileIterator* cpp_iterator

    def __cinit__(self, int fileno, int pos):
        self.cpp_iterator = new FileIterator(fileno, pos)

    def __dealloc__(self):
        del self.cpp_iterator

    def grep(self, string  key, size_t ilen, size_t ishift):

        cdef int ierr
        # vector
        cdef vector[string] vec
        vec.reserve(ilen)
        # grep
        ierr = self.cpp_iterator.grep(key, ilen, ishift, vec)
        return ierr, vec

    def seek(self, const int offset):
        return self.cpp_iterator.seek(offset) 

    def tell(self):
        return self.cpp_iterator.tell() 


class Iterator(object):

    def __init__(self, filename, option='r'):
        self.f = open(filename, option)
        self.cpp_iterator = PyFileIterator(self.fileno, self.tell)

    def __enter__(self):
        return self

    @property
    def tell(self):
        return self.f.tell()

    def seek(self, val):
        self.f.seek(val)

    @property
    def filehandle(self):
        return self.f

    @property
    def fileno(self):
        return self.f.fileno()

    def __del__(self):            
        if not self.f.closed:
            self.f.close()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        line = self.f.readline()
        if not line:
            raise StopIteration
        return line

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def grep(self, string  key, size_t ilen, size_t ishift):

        cdef int ierr
        cdef vector[string] vec


        with FileContextManager(self):
            ierr, vec= self.cpp_iterator.grep(key, ilen, ishift)

        return vec, ierr
        
