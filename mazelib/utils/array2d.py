
from array import array


class Array2D(object):
    """
    A simple interface to mimic a two-dimensional array in Python.
    The goal is to save me from an import of the entire NumPy library.
    """

    ALLOWED_TYPECODES = ['c', 'b', 'B', 'u', 'h', 'H', 'i', 'I', 'l', 'L', 'f', 'd']
    BOUND_ERROR = 'array assignment index out of range'
    LENGTH_ERROR = 'input values were the wrong length'
    VAL_TYPE_ERROR = 'input values were the wrong type'
    INX_TYPE_ERROR = 'array assignment index was the wrong type'
    TYPECODE_ERROR = 'bad typecode (must be in: %s) ' % ', '.join(ALLOWED_TYPECODES)

    def __init__(self, typecode, shape, fill_value=None):
        if typecode not in Array2D.ALLOWED_TYPECODES:
            raise ValueError(Array2D.TYPECODE_ERROR)

        (h, w) = shape
        if fill_value is None:
            if typecode == 'c':
                fill_value = '0'
            elif typecode == 'u':
                fill_value = u'0'
            else:
                fill_value = 0

        self._array = array(typecode, [fill_value] * h * w)
        self.typecode = typecode
        self.height = h
        self.width = w

    def __getitem__(self, ind):
        """
        This method allows the Array2D data structure to use
        the Python standard [ ] notation to get values.
        """
        if isinstance(ind, int):
            """ If index is an int, return a single row """
            if ind >= 0 and ind < self.height:
                return self._array[ind * self.width: ind * self.width + self.width]
            else:
                raise ValueError(Array2D.BOUND_ERROR)
        elif isinstance(ind, tuple):
            """ If index is a tuple, return a single value """
            row, col = ind
            if row < 0 or row >= self.height:
                raise ValueError(Array2D.BOUND_ERROR)
            elif col < 0 or col >= self.width:
                raise ValueError(Array2D.BOUND_ERROR)
            else:
                row, col = ind
                return self._array[row * self.width + col]
        elif isinstance(ind, slice):
            """ If index is a slice object, return a single value """
            start, stop, step = ind.indices(self.height)
            if start < 0 or stop > self.height:
                raise ValueError(Array2D.BOUND_ERROR)
            elif not step or step == 1:
                """ slice is one continuous block """
                out = Array2D(self.typecode, (stop - start, self.width))
                for row in xrange(0, stop - start):
                    out._array[row * out.width: row * out.width + out.width] = self[row + start]
                return out
            else:
                """ discontinous rows are being sliced """
                num_steps = len(xrange(start, stop, step))
                out = Array2D(self.typecode, (num_steps, self.width))
                for i,j in enumerate(xrange(start, stop, step)):
                    out[i * out.width: i * out.width + out.width] = self[j]
                return out
        else:
            raise TypeError(Array2D.INX_TYPE_ERROR)

    def __setitem__(self, ind, value):
        """
        This method allows the Array2D data structure to use
        the Python standard [ ] notation to set values.
        """
        # TODO: This method is too long. Perhaps I can use __setslice__ to organize this?
        if isinstance(ind, int):
            """ If index is an int, set a single row """
            if ind >= 0 and ind < self.height:
                if isinstance(value, array):
                    """ replace row with array """
                    if len(value) == self.width:
                        self._array[ind * self.width: ind * self.width + self.width] = value
                    else:
                        raise ValueError(Array2D.LENGTH_ERROR)
                elif issubclass(type(value), Array2D):
                    """ replace row with Array2D or subclass """
                    if value.height == 1:
                        self._array[ind * self.width: ind * self.width + self.width] = value._array
                    else:
                        raise ValueError(Array2D.LENGTH_ERROR)
                elif isinstance(value, list) or isinstance(value, tuple):
                    """ replace row with list or tuple """
                    if len(value) == self.width:
                        self._array[ind * self.width: ind * self.width + self.width] = \
                            array(self.typecode, value)
                    else:
                        raise ValueError(Array2D.LENGTH_ERROR)
                else:
                    raise TypeError(Array2D.VAL_TYPE_ERROR)
            else:
                raise ValueError(Array2D.BOUND_ERROR)
        elif isinstance(ind, tuple):
            """ If index is a tuple, set a single value """
            row, col = ind
            if isinstance(col, slice):
                if not hasattr(row, '__iter__'): row = [row]
                col = slice(0 if col.start is None else col.start, \
                            self.width if col.stop is None else col.stop, \
                            1 if col.step is None else col.step)
                for r in row:
                    if not hasattr(value, '__iter__'):
                        for c in xrange(col.start, col.stop, col.step):
                            self._array[r * self.width + c] = value
                    else:
                        for i,c in enumerate(xrange(col.start, col.stop, col.step)):
                            self._array[r * self.width + c] = value[i]
            elif isinstance(row, slice):
                if col == -1: col = self.width - 1
                if not hasattr(col, '__iter__'): col = [col]
                row = slice(0 if row.start is None else row.start, \
                            self.height if row.stop is None else row.stop, \
                            1 if row.step is None else row.step)
                for c in col:
                    if not hasattr(value, '__iter__'):
                        for r in xrange(row.start, row.stop, row.step):
                            self._array[r * self.width + c] = value
                    else:
                        for i,r in enumerate(xrange(row.start, row.stop, row.step)):
                            self._array[r * self.width + c] = value[i]
            else:
                if row < 0 or row > self.height:
                    raise ValueError(Array2D.BOUND_ERROR)
                elif col < 0 or col >= self.width:
                    raise ValueError(Array2D.BOUND_ERROR)
                elif type(value) != type(self._array[0]):
                    raise TypeError(Array2D.VAL_TYPE_ERROR)
                self._array[row * self.width + col] = value
        elif isinstance(ind, slice):
            """ If the index is a slice object, set multiple rows """
            start, stop, step = ind.indices(self.height)
            if start < 0 or stop >= self.height:
                raise ValueError(Array2D.BOUND_ERROR)
            elif not step or step == 1:
                """ slice is one continuous block """
                if isinstance(value, array):
                    """ replace rows with array """
                    if len(value) == (stop - start) * self.width:
                        self._array[start * self.width: stop * self.width + self.width] = value
                    else:
                        raise ValueError(Array2D.LENGTH_ERROR)
                elif issubclass(type(value), Array2D):
                    """ replace rows with Array2D or subclass """
                    if len(value._array) == (stop - start) * self.width:
                        self._array[start * self.width: stop * self.width + self.width] = value._array
                    else:
                        raise ValueError(Array2D.LENGTH_ERROR)
                elif isinstance(value, list) or isinstance(value, tuple):
                    """ replace rows with list or tuple (TODO: could be any iterable?) """
                    if len(value) == (stop - start) * self.width:
                        self._array[start * self.width: stop * self.width + self.width] = \
                            array(self.typecode, value)
                    else:
                        raise ValueError(Array2D.LENGTH_ERROR)
                else:
                    raise TypeError(Array2D.VAL_TYPE_ERROR)
            else:
                """ discontinous rows are being sliced """
                num_steps = len(xrange(start, stop, step))
                if isinstance(value, list) or isinstance(value, tuple):
                    """ replace rows with list or tuple of list/tuple/arrays """
                    if len(value) != num_steps:
                        raise ValueError(Array2D.LENGTH_ERROR)
                    elif type(value[0][0]) != type(self._array[0]):
                        raise TypeError(Array2D.VAL_TYPE_ERROR)

                    for row in xrange(0, num_steps):
                        if len(value[row]) != self.width:
                            raise ValueError(Array2D.LENGTH_ERROR)

                    for i,j in enumerate(xrange(start, stop, step)):
                        self._array[j * self.width: j * self.width + self.width] = \
                            array(self.typecode, value[i])
                if isinstance(value, array):
                    """ replace rows with array """
                    if len(value) != num_steps * self.width:
                        raise ValueError(Array2D.LENGTH_ERROR)
                    elif type(value[0]) != type(self._array[0]):
                        raise TypeError(Array2D.VAL_TYPE_ERROR)

                    for i,j in enumerate(xrange(start, stop, step)):
                        self._array[j * self.width: j * self.width + self.width] = value[i]
                if issubclass(type(value), Array2D):
                    """ replace rows with Array2D or subclass """
                    if value.height != num_steps:
                        raise ValueError(Array2D.LENGTH_ERROR)
                    elif value.width != self.width:
                        raise ValueError(Array2D.LENGTH_ERROR)
                    elif value.typecode != self.typecode:
                        raise TypeError(Array2D.VAL_TYPE_ERROR)

                    for i,j in enumerate(xrange(start, stop, step)):
                        self._array[j * self.width: j * self.width + self.width] = \
                            value._array[i * value.width: i * value.width + value.width]
                else:
                    raise TypeError(Array2D.VAL_TYPE_ERROR)
        else:
            raise TypeError(Array2D.INX_TYPE_ERROR)

    def __str__(self):
        s = '['
        for row in xrange(self.height):
            s += '[' if row == 0 else ' ['

            for col in xrange(self.width):
                s += str(self._array[row * self.width + col])
                s += ','
            s = s[:-1]
            s += ']\n'

        s = s[:-1]
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
        i = 0
        while i < self.height:
            yield self.__getitem__(i)
            i += 1
