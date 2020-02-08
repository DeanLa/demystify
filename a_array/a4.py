"""Shapes"""


class Arr:
    def __init__(self, data):
        data = [item for item in data]
        self.dtype = dtype(data)
        self.data = [self.dtype(item) for item in data]
        self.size = len(self.data)
        self.reshape(self.size)
        self.start = 0

    def reshape(self, rows, cols=None):
        if cols is None:
            self.reshape(rows, 1)
            self.shape = (self.shape[0],)
            self.ndim = len(self.shape)
            return self
        elif cols == -1:
            assert self.size % rows == 0, f"rows must be divide {self.size} without a remainder"
            cols = self.size // rows
        assert rows * cols == len(self.data), (f"cannot reshape data with {self.size}"
                                               f" values to shape ({rows},{cols})")
        self.shape = (rows, cols)
        self.ndim = len(self.shape)
        # self.strides = (self.shape[1], 1)
        return self

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

    def __getitem__(self, item):
        return self.data[item]




# def num_to_slice(num, other_axis):
#     return slice(num * other_axis, num * other_axis - 1)


def zip_apply(left, right, f):
    # Length is the same
    assert len(left) == len(right), f'arrays are not of same shape'
    # Type is the same
    assert dtype(left) == dtype(right), f'Arrays are not of same dtype'
    # We can do the work
    result = [f(l, r) for (l, r) in zip(left, right)]
    return Arr(result)


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
    a = Arr([1, 2, 3, 4, 5, 6])
    a.reshape(3, 2)
    print (a)
    a = Arr(range(64)).reshape(8, -1)
    print (a)
    b = a[0:2   :2, 1]
    a.reshape(6)
