class GI():
    def __init__(self):
        self.data = [1, 2, 3, 4, 5, 6]

    def __getitem__(self, item):
        print(item)
        return self.data[item]


a = GI()
x = a[1]
x = a[-1]
# Slices
x = a[1:4]
x = a[:4]
x = a[4:]
x = a[::]
x = a[::2]

###
print(slice(1))
print(slice(1, 2))
print(slice(1, 2, 3))

###
sl = slice(4)
print(sl)
print(sl.indices(7))
sl = slice(None, None, 4)
print(sl)
print(sl.indices(7))

###
y = a[:4, :2]
