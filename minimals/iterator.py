class It():
    def __init__(self):
        self.data = [1, 2, 3, 4, 5, 6]
        self.start = 0
        self._index = self.start

    def __next__(self):
        ret = self.data[self._index]
        if ret > 4:
            raise StopIteration
        self._index += 1
        return ret

    def __iter__(self):
        self._index = self.start
        return self


it = It()
for i in it:
    print(i)
print('One')  # Try to comment out first line of __iter__
for i in it:
    print(i)
print('Two')
for i in it:  # Will not work as expected - why?
    for j in it:
        print(f'{i}---{j}')
print()
