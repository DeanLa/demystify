"""Broadcasting"""


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
            ret += str(self.data)
        else:
            rows, cols = self.shape
            for i, val in enumerate(self.data):
                ret += str(val).center(6)
                if i % cols - cols == -1:
                    ret += '\n'

        return ret

    __repr__ = __str__

    def __getitem__(self, items):
        if not hasattr(items, '__len__'):
            items = (items,)
        assert self.ndim >= len(items), 'More slicers than ndim'
        if self.ndim == 1:
            return self.data[items[0]]

        if self.ndim > len(items):
            # Bring only rows
            ret = self.__getitem__((*items, slice(None)))
            return ret
        ret = []
        # rows
        r_start, r_stop, r_step = items[0].indices(self.shape[0])
        c_start, c_stop, c_step = items[1].indices(self.shape[1])
        new_shape = (indices2len(r_start, r_stop, r_step), indices2len(c_start, c_stop, c_step))
        r_index, c_index = r_start, c_start
        while True:
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
        ret = Arr(ret)
        ret.reshape(*new_shape)
        return ret

    def _coord2idx(self, row, col):
        return row * self.shape[1] + col

    def _idx2coord(self, idx):
        row = idx // self.shape[1]
        col = idx % self.shape[0]
        return row, col

    ### Math
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


def indices2len(start, stop, step):
    return (stop - start - 1) // step + 1


def align(x, y):
    if x.ndim == y.ndim:
        return x, y
    elif x.ndim < y.ndim:
        x = x.reshape(1, *x.shape)
        return align(x, y)
    else:
        y, x = align(y, x)
        return x, y


def broadcast(x, y):
    return x, y


def zip_apply(left, right, f):
    # Shape is the compatible
    left, right = align(left, right)
    left, right = broadcast(left, right)
    assert left.shape == right.shape, f'arrays are not of same shape'
    # Type is the same
    assert dtype(left) == dtype(right), f'Arrays are not of same dtype'
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
    b = a.reshape(8, -1)
    b2 = b.reshape(-1, )
    print(b2)
    c = Arr(range(100, 900, 100))
    d, e = align(b, b)
    d, e = align(b, c)
    d, e = align(b, c.reshape(-1, 1))
    d, e = align(c, b)
