"""zip_apply to make arithmetic generic"""



class Arr:
    def __init__(self, data):
        data = [item for item in data]
        self.dtype = dtype(data)
        self.data = [self.dtype(item) for item in data]

    def __str__(self):
        return (f"Arr: {self.data}")

    __repr__ = __str__

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

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
        return Arr(map(self.dtype.__abs__, self.data))


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
    a = Arr([1, 2])
    b = Arr([-3, 4])
    for i in a:
        print(i)
    print(a + b)
    print(a - b)
    print(abs(a - b))
    print(a * b)
    print(a / b)
