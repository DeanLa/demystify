class Arr:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return (f"Arr: {self.data}")

    __repr__ = __str__

    def __add__(self, other):
        L = self.data
        R = other.data
        res = []
        for l, r in zip(L,R):
            res.append(l+r)
        return Arr(res)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

def array_adder(left, right):
    # Length is the same
    assert len(left) == len(right), f'arrays are not of the shape'
    # Type is the same
    assert left.dtype == right.dtype
if __name__ == '__main__':
    a = Arr([1,2])
    b = Arr([3,4])
    print (a)
    print()