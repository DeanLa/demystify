"""More Robust addition function"""


class Arr:
    def __init__(self, data):
        self.dtype = dtype(data)
        self.data = [self.dtype(item) for item in data]

    def __str__(self):
        return (f"Arr: {self.data}")

    __repr__ = __str__

    def __add__(self, other):
        return array_adder(self, other)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]



def array_adder(left, right):
    # Length is the same
    assert len(left) == len(right), f'arrays are not of same shape'
    # Type is the same
    assert dtype(left) == dtype(right), f'Arrays are not of same dtype'
    # We can do the work
    result = [l + r for (l, r) in zip(left, right)]
    return result


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
    i1 = Arr([1, 2])
    i2 = Arr([3, 4])
    f = Arr([3, 4.0])
    s1 = Arr([10, 20, '30'])
    s2 = Arr(['a', 'b', 'c'])
    print(i1 + i2)
    print(s1 + s2)
