"""Slicing"""


class Arr:
    def __init__(self, data):
        data = [item for item in data]
        self.dtype = dtype(data)
        self.data = [self.dtype(item) for item in data]
        self.size = len(self.data)
        self.shape = (self.size,)
        self.ndim = 1

    def reshape(self, rows, cols=None):
        ret = Arr(self.data)
        if cols is None:
            ret = ret.reshape(rows, 1)
            ret.shape = (ret.shape[0],)
            ret.ndim = len(ret.shape)
            return ret
        elif cols == -1:
            assert self.size % rows == 0, f"rows must be divide {self.size} without a remainder"
            cols = self.size // rows
        elif rows == -1:
            assert self.size % cols == 0, f"cols must be divide {self.size} without a remainder"
            rows = self.size // cols
        assert rows * cols == len(self.data), (f"cannot reshape data with {self.size}"
                                               f" values to shape ({rows},{cols})")
        ret.shape = (rows, cols)
        ret.ndim = len(ret.shape)
        return ret

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        ret = "Arr: \n"
        if self.ndim < 2:
            data = self.reshape(1, -1).data
            cols = len(data)
        else:
            data = self.data
            cols = self.shape[1]
        for i, val in enumerate(data):
            ret += str(val).center(6)
            if i % cols - cols == -1:
                ret += '\n'

        return ret

    __repr__ = __str__

    def __getitem__(self, items):
        if not isinstance(items, tuple):  # got only one slicer
            items = (items,)
        assert self.ndim >= len(items), 'More slicers than ndim'
        if self.ndim == 1:
            return self.data[items[0]]

        if self.ndim > len(items):
            # Bring only rows
            ret = self.__getitem__((*items, slice(None)))
            return ret
        r_start, r_stop, r_step = items[0].indices(self.shape[0])
        c_start, c_stop, c_step = items[1].indices(self.shape[1])
        new_shape = (indices2len(r_start, r_stop, r_step), indices2len(c_start, c_stop, c_step))
        return self.array_iterator(new_shape, r_start, r_step, r_stop, c_step, c_stop, c_start)

    def broadcast(self, new_shape):
        if self.ndim < 2:
            ret = self.reshape(1, *(self.shape))
            ret = ret.broadcast((1, *new_shape))
            return ret.reshape(-1)
        r_start = 0
        r_stop = new_shape[0]
        r_step = self.shape[0] // new_shape[0]
        c_start = 0
        c_stop = new_shape[1]
        c_step = self.shape[1] // new_shape[1]
        return self.array_iterator(new_shape, r_start, r_step, r_stop, c_step, c_stop, c_start)

    def array_iterator(self, new_shape, r_start, r_step, r_stop, c_step, c_stop, c_start):
        r_index, c_index = r_start, c_start
        ret = []
        for _ in range(new_shape[0] * new_shape[1]):
            if c_index >= c_stop:
                c_index = c_start
                r_index += r_step
            if r_index >= r_stop:
                break
            _index = self._coord2idx(r_index, c_index)
            try:
                ret.append(self.data[_index])
            except IndexError:
                break
            c_index += c_step
        ret = Arr(ret).reshape(*new_shape)
        return ret

    def _coord2idx(self, row, col):
        return row * self.shape[1] + col

    def _idx2coord(self, idx):
        row = idx // self.shape[1]
        col = idx % self.shape[0]
        return row, col

    ### Math
    def sum(self):
        return sum(self)

    def count(self):
        return len(self)

    def mean(self):
        return (self.sum() / self.count())

    ### Arithmetic
    def __add__(self, other):
        return zip_apply(self, other, self.dtype.__add__)

    def __sub__(self, other):
        return zip_apply(self, other, self.dtype.__sub__)

    def __mul__(self, other):
        return zip_apply(self, other, self.dtype.__mul__)

    def __truediv__(self, other):
        return zip_apply(self, other, self.dtype.__truediv__)

    def __abs__(self):
        return map(self.dtype.__abs__, self.data)

    def __len__(self):
        return self.shape[0]


def get_slice_indices(sl, shape):
    if sl.step != 0:
        pass
    else:
        pass


def indices2len(start, stop, step):
    if step > 0:
        return (stop - start - 1) // step + 1
    elif step == 0:
        return 1
    else:
        raise ValueError


def align(x, y):
    if x.ndim < y.ndim:
        x = x.reshape(1, *x.shape)
        x, y = align(x, y)
    elif x.ndim > y.ndim:
        y, x = align(y, x)
    # Else they are equal and just return them
    return x, y


def _compatible_shapes(x, y):
    if x.ndim != y.ndim:
        return False
    for xi, yi in zip(x.shape, y.shape):
        if xi == 1 or yi == 1 or xi == yi:
            continue
        else:
            return False
    return True


def broadcast_arrays(x, y):
    assert _compatible_shapes(x, y), f'cannot broadcast shapes {x.shape} and {y.shape}'
    new_shape = tuple([max(xi, yi) for xi, yi in zip(x.shape, y.shape)])
    x = broadcast(x, new_shape)
    y = broadcast(y, new_shape)
    return x, y


def broadcast(arr, shape):
    return arr.broadcast(shape)


def zip_apply(left, right, f):
    if not isinstance(right, Arr):
        assert isinstance(right, dtype(left))
        right = Arr([right])
    # Type is the same
    assert dtype(left) == dtype(right), f'Arrays are not of same dtype'
    # Shape is the compatible
    left, right = align(left, right)
    left, right = broadcast_arrays(left, right)
    assert left.shape == right.shape, f'Broadcasting went wrong'
    # We can do the work
    result = [f(l, r) for (l, r) in zip(left, right)]
    return Arr(result).reshape(*left.shape)


def dtype(obj):
    """Returns the dtype of the array"""
    dtype = int
    for item in obj:
        itype = type(item)
        if itype == str:  # str is the largest, so dtype is str
            return str
        if itype == float:  # We haven't seen str by now so type is either float or int
            dtype = float
    return dtype


if __name__ == '__main__':
    a = Arr(range(64))
    print(a[3])
    b = a.reshape(8, -1)
    c = Arr(range(100, 900, 100))
    print(b + c)
    d = Arr([1000])
    print(b + d)
    b2 = b[1:2]
