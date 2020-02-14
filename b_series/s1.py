from a_array.array import Arr
from collections import defaultdict


class Idx:
    def __init__(self, data):
        self.values = Arr(data)
        self.mapping = defaultdict(list)
        for i, key in enumerate(data):
            self.mapping[key].append(i)

    def __getattr__(self, item):
        return getattr(self.values, item)

    def __getitem__(self, item):
        return self.values.__getitem__(item)

    def __iter__(self):
        return iter(self.values)

    __len__ = lambda self: len(self.values)

    def unique(self):
        return Arr(self.mapping.keys())


class Srs:
    def __init__(self, data, name=None, index=None):
        self.values = Arr(data)
        self.index = index or Idx(range(len(data)))
        assert len(self.values) == len(self.index)
        self.name = name or "new_series"

    def __iter__(self):
        return zip(self.index.values, self.values)

    __len__ = lambda self: len(self.values)

    def __str__(self):
        ret = f"{self.name}: \n"
        for idx, val in self:
            ret += str(idx).center(6)
            ret += str(val).center(6)
            ret += '\n'

        return ret

    __repr__ = __str__

    def __add__(self, other):
        return Srs(self.values.__add__(other.values), index=self.index)

    def __getattr__(self, item):
        if hasattr(self.values, item):
            return getattr(self.values, item)
        raise AttributeError

    def __getitem__(self, items):
        if items == slice(None):
            return self
        items = listify(items)
        idx = []
        for item in items:
            assert item in self.index, f'{items} is not in the series index'
            idx.extend(self.index.mapping.get(item))

        idx = sorted(idx)
        vals = [self.values[i] for i in idx]
        new_index = [self.index[i] for i in idx]
        return Srs(vals, name=self.name, index=Idx(new_index))

    def as_index(self):
        return Idx(self.values)

    def value_counts(self):
        idx = self.as_index()
        map_ = idx.mapping
        keys = []
        counts = []
        for key, indices in map_.items():
            keys.append(key)
            counts.append(len(indices))
        ret = Srs(counts, name=f'{self.name} value counts', index=Idx(keys))
        return ret


def listify(val):
    if isinstance(val, list):
        return val
    else:
        return [val]


if __name__ == '__main__':
    idx = Idx(list('abcde'))
    s = Srs(range(5), 'foo', idx)
    print(s['a'])
    idx = Idx(list('abede'))
    z = Srs(range(5), 'bar', idx)
    print(z[['e']])
    print(z[['e', 'a']])
    print (z.value_counts())
    vc = Srs('abbbbabdbedb', name='letters')
    print(vc)
    print(vc.value_counts())
