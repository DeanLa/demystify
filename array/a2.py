class Arr:
    def __init__(self, data):
        self.data = data
        self.dtype = dtype(self)

    def __str__(self):
        return (f"Arr: {self.data}")

    __repr__ = __str__

    def __add__(self, other):
        array_adder(self, other)

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
    result = [l + r for (l,r) in zip(left,right)]
    return result

def dtype(obj):
    """Returns the dtype of the array"""
    dtype = int
    for item in obj:
        itype =  type(item)
        if itype == str: # str is the largest, so dtype is str
            return str
        if itype == float: # We haven't seen str by now so type is either float or int
            dtype = float
    return dtype


if __name__ == '__main__':
    a = Arr([1,2])
    b = Arr([3,4])
    c = Arr([3,4.0])
    d = Arr([10,20,'30'])
    s = Arr(['a','b','c'])
    print (d+s)
    print()