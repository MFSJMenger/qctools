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
        vector[string] grep(const string& key, size_t ilen, const size_t ishift, int& ierr)
        vector[string] in_between(const string& start, const string& end, int& ierr)
        vector[string] till(const string& end, int& ierr)
        int seek(const int offset) 
        int tell()


class FileContextManager(object):

    def __init__(self, iterator):
        self._iterator = iterator

    def __enter__(self):
        # update cpp iterator
        self._iterator.iterator.seek(self._iterator.iterator.tell())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # update normal iterator
        self._iterator.seek(self._iterator.iterator.tell())



cdef class PyFileIterator:

    # python wrapper for FileIterator 

    cdef FileIterator* _iterator

    def __cinit__(self, int fileno, int pos):
        self._iterator = new FileIterator(fileno, pos)

    def __dealloc__(self):
        del self._iterator

    def grep(self, const string key, size_t ilen, const size_t ishift):

        cdef int ierr
        # vector
        cdef vector[string] vec
        # grep
        vec = self._iterator.grep(key, ilen, ishift, ierr)
        # return
        return ierr, vec

    def in_between(self, const string start, const string end):

        cdef int ierr
        # vector
        cdef vector[string] vec
        # grep
        vec = self._iterator.in_between(start, end, ierr)
        # return
        return ierr, vec

    def till(self, const string end):

        cdef int ierr
        # vector
        cdef vector[string] vec
        # grep
        vec = self._iterator.till(end, ierr)
        # return
        return ierr, vec

    def seek(self, const int offset):
        return self._iterator.seek(offset) 

    def tell(self):
        return self._iterator.tell() 


class Iterator(object):

    def __init__(self, filename, option='r'):
        self.f = open(filename, option)
        self._iterator = PyFileIterator(self.fileno, self.tell)

    def __del__(self):            
        if not self.f.closed:
            self.f.close()

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
    def iterator(self):
        return self._iterator

    @property
    def fileno(self):
        return self.f.fileno()

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

    def grep(self, const string key, size_t ilen, const size_t ishift):

        cdef int ierr
        cdef vector[string] vec

        with FileContextManager(self):
            ierr, vec = self._iterator.grep(key, ilen, ishift)

        return vec, ierr
        
    def in_between(self, const string start, const string end):

        cdef int ierr
        cdef vector[string] vec

        with FileContextManager(self):
            ierr, vec = self._iterator.in_between(start, end)

        return vec, ierr

    def till(self, const string end):

        cdef int ierr
        cdef vector[string] vec

        with FileContextManager(self):
            ierr, vec = self._iterator.till(end)

        return vec, ierr
