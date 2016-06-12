
from array import array

cdef const char* BOUND_ERROR = 'array assignment index out of range'
cdef const char* INX_TYPE_ERROR = 'array assignment index was the wrong type'
cdef const char* LENGTH_ERROR = 'input values were the wrong length'
cdef const char* VAL_TYPE_ERROR = 'input values were the wrong type'
cdef unicode TYPECODE = u'b'  # TODO: Should be constant...


cdef class MazeArray(object):
    """
    TODO
    A simple interface to mimic a two-dimensional array in Python.
    The goal is to save me from an import of the entire NumPy library.

    TODO:
    To convert _array to a c-array, you will need to (at least)
    implement slicing on the c-array.  (Ignore numpy).)
    """

    cdef object _array  # TODO: Change this to C array
    cdef public int height
    cdef public int width

    def __cinit__(self, int h, int w, bint default_value=True):
        self._array = array(TYPECODE, [default_value] * h * w)
        self.height = h
        self.width = w

    def __init__(self, int h, int w, bint default_value=True):
        pass

    def __dealloc__(self):
        pass

    cpdef copy(self):
        ''' This is a non-standard deepcopy implementation
            that should be safe for Cython, Python v2.x and
            Python v3.x.
        '''
        cdef int i

        ma = MazeArray(self.height, self.width)
        for i in range(len(self._array)):
            ma._array[i] = self._array[i]

        return ma

    def __getitem__(self, ind):
        """
        This method allows the MazeArray data structure to use
        the Python standard [ ] notation to get values.
        """
        cdef int row, col, start, stop, step, num_steps
        if isinstance(ind, int):
            # If index is an int, return a single row
            if ind >= 0 and ind < self.height:
                return self._array[ind * self.width: ind * self.width + self.width]
            else:
                raise ValueError(BOUND_ERROR)
        elif isinstance(ind, tuple):
            # If index is a tuple, return a single value
            row, col = ind
            if row < 0 or row >= self.height:
                raise ValueError(BOUND_ERROR)
            elif col < 0 or col >= self.width:
                raise ValueError(BOUND_ERROR)
            else:
                row, col = ind
                return self._array[row * self.width + col]
        elif isinstance(ind, slice):
            # If index is a slice object, return a single value
            start, stop, step = ind.indices(self.height)
            if start < 0 or stop > self.height:
                raise ValueError(BOUND_ERROR)
            elif not step or step == 1:
                # slice is one continuous block
                out = MazeArray((stop - start, self.width))
                for row in range(0, stop - start):
                    out._array[row * out.width: row * out.width + out.width] = self[row + start]
                return out
            else:
                # discontinous rows are being sliced
                num_steps = len(range(start, stop, step))
                out = MazeArray((num_steps, self.width))
                for i, j in enumerate(range(start, stop, step)):
                    out[i * out.width: i * out.width + out.width] = self[j]
                return out
        else:
            raise TypeError(INX_TYPE_ERROR)

    def __setitem__(self, ind, value):
        """
        This method allows the MazeArray data structure to use
        the Python standard [ ] notation to set values.
        """
        cdef int start, stop, step, num_steps
        # TODO: This method is too long. Perhaps I can use __setslice__ to organize this?
        if isinstance(ind, int):
            # If index is an int, set a single row
            if ind >= 0 and ind < self.height:
                if isinstance(value, array):
                    # replace row with array
                    if len(value) == self.width:
                        self._array[ind * self.width: ind * self.width + self.width] = value
                    else:
                        raise ValueError(LENGTH_ERROR)
                elif issubclass(type(value), MazeArray):
                    # replace row with MazeArray or subclass
                    if value.height == 1:
                        self._array[ind * self.width: ind * self.width + self.width] = value._array
                    else:
                        raise ValueError(LENGTH_ERROR)
                elif isinstance(value, list) or isinstance(value, tuple):
                    # replace row with list or tuple
                    if len(value) == self.width:
                        self._array[ind * self.width: ind * self.width + self.width] = \
                            array(TYPECODE, value)
                    else:
                        raise ValueError(LENGTH_ERROR)
                else:
                    raise TypeError(VAL_TYPE_ERROR)
            else:
                raise ValueError(BOUND_ERROR)
        elif isinstance(ind, tuple):
            # If index is a tuple, set a single value
            row, col = ind
            if isinstance(col, slice):
                if not hasattr(row, '__iter__'):
                    row = [row]
                col = slice(0 if col.start is None else col.start, \
                            self.width if col.stop is None else col.stop, \
                            1 if col.step is None else col.step)
                for r in row:
                    if not hasattr(value, '__iter__'):
                        for c in range(col.start, col.stop, col.step):
                            self._array[r * self.width + c] = value
                    else:
                        for i,c in enumerate(range(col.start, col.stop, col.step)):
                            self._array[r * self.width + c] = value[i]
            elif isinstance(row, slice):
                if col == -1:
                    col = self.width - 1
                if not hasattr(col, '__iter__'): col = [col]
                row = slice(0 if row.start is None else row.start, \
                            self.height if row.stop is None else row.stop, \
                            1 if row.step is None else row.step)
                for c in col:
                    if not hasattr(value, '__iter__'):
                        for r in range(row.start, row.stop, row.step):
                            self._array[r * self.width + c] = value
                    else:
                        for i, r in enumerate(range(row.start, row.stop, row.step)):
                            self._array[r * self.width + c] = value[i]
            else:
                if row < 0 or row > self.height:
                    raise ValueError(BOUND_ERROR)
                elif col < 0 or col >= self.width:
                    raise ValueError(BOUND_ERROR)
                elif type(value) != type(self._array[0]):
                    raise TypeError(VAL_TYPE_ERROR)
                self._array[row * self.width + col] = value
        elif isinstance(ind, slice):
            # If the index is a slice object, set multiple rows
            start, stop, step = ind.indices(self.height)
            if start < 0 or stop >= self.height:
                raise ValueError(BOUND_ERROR)
            elif not step or step == 1:
                # slice is one continuous block
                if isinstance(value, array):
                    # replace rows with array
                    if len(value) == (stop - start) * self.width:
                        self._array[start * self.width: stop * self.width + self.width] = value
                    else:
                        raise ValueError(LENGTH_ERROR)
                elif issubclass(type(value), MazeArray):
                    # replace rows with MazeArray or subclass
                    if len(value._array) == (stop - start) * self.width:
                        self._array[start * self.width: stop * self.width + self.width] = value._array
                    else:
                        raise ValueError(LENGTH_ERROR)
                elif isinstance(value, list) or isinstance(value, tuple):
                    # replace rows with list or tuple (TODO: could be any iterable?)
                    if len(value) == (stop - start) * self.width:
                        self._array[start * self.width: stop * self.width + self.width] = \
                            array(TYPECODE, value)
                    else:
                        raise ValueError(LENGTH_ERROR)
                else:
                    raise TypeError(VAL_TYPE_ERROR)
            else:
                # discontinous rows are being sliced
                num_steps = len(range(start, stop, step))
                if isinstance(value, list) or isinstance(value, tuple):
                    # replace rows with list or tuple of list/tuple/arrays
                    if len(value) != num_steps:
                        raise ValueError(LENGTH_ERROR)
                    elif type(value[0][0]) != type(self._array[0]):
                        raise TypeError(VAL_TYPE_ERROR)

                    for row in range(0, num_steps):
                        if len(value[row]) != self.width:
                            raise ValueError(LENGTH_ERROR)

                    for i,j in enumerate(range(start, stop, step)):
                        self._array[j * self.width: j * self.width + self.width] = \
                            array(TYPECODE, value[i])
                if isinstance(value, array):
                    # replace rows with array
                    if len(value) != num_steps * self.width:
                        raise ValueError(LENGTH_ERROR)
                    elif type(value[0]) != type(self._array[0]):
                        raise TypeError(VAL_TYPE_ERROR)

                    for i, j in enumerate(range(start, stop, step)):
                        self._array[j * self.width: j * self.width + self.width] = value[i]
                if issubclass(type(value), MazeArray):
                    # replace rows with MazeArray or subclass
                    if value.height != num_steps:
                        raise ValueError(LENGTH_ERROR)
                    elif value.width != self.width:
                        raise ValueError(LENGTH_ERROR)
                    elif value.typecode != TYPECODE:
                        raise TypeError(VAL_TYPE_ERROR)

                    for i,j in enumerate(range(start, stop, step)):
                        self._array[j * self.width: j * self.width + self.width] = \
                            value._array[i * value.width: i * value.width + value.width]
                else:
                    raise TypeError(VAL_TYPE_ERROR)
        else:
            raise TypeError(INX_TYPE_ERROR)

    def __str__(self):
        s = '['
        for row in range(self.height):
            s += '[' if row == 0 else ' ['

            for col in range(self.width):
                s += str(self._array[row * self.width + col])
                s += ','
            s = s[:-1]
            s += '],\n'

        s = s[:-2]
        if not s:
            return '[]\n'
        s += ']\n'

        return s

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        """ returns the length as if it were a 1D array """
        return self.width * self.height

    def __iter__(self):
        return self._iterate()

    def _iterate(self):
        cdef int i
        i = 0
        while i < self.height:
            yield self.__getitem__(i)
            i += 1
