from functools import partial

from b_series.s1 import Srs, Idx
from a_array.array import Arr


class DF():
    def __init__(self, data, index=None):
        self.index = index or Idx(range(len(self)))
        self._validate(data)
        self.columns = []
        self.data = {}
        for name, vals in data.items():
            self.columns.append((name))
            if isinstance(vals, Srs):
                vals = vals.values
            self.data[name] = Srs(vals, name=name, index=self.index)

    def _validate(self, data):
        self.shape = (len(self.index), len(data.keys()))
        for col in data.values():
            assert len(col) == self.shape[0], "Not all columns are of same length"

    def __len__(self):
        return self.shape[0]

    def __str__(self):
        maxlen = max([len(col_name) for col_name in self.columns]) + 2
        maxlen = max(maxlen, 8)
        ret = ''.center(maxlen)
        for col_name in self.columns:
            ret += col_name.center(maxlen)
        ret += '\n'
        for row in self.iterrows():
            for cell in row:
                ret += str(cell).center(maxlen)
            ret += '\n'
        return ret

    def __repr_markdown__(self):
        # Exercise
        pass

    __repr__ = __str__

    def __getitem__(self, items):
        if not isinstance(items, tuple):
            items = (items,)
        if len(items) == 1:
            return self[:, items[0]]
        colidx = items[1]
        if colidx == slice(None):
            columns = self.columns
        elif isinstance(colidx, str):
            return self.data[colidx]
        else:
            columns = [col for col in self.columns if col in colidx]
        data = {col: self.data[col][items[0]] for col in columns}
        index = data[columns[0]].index
        ret = DF(data, index=index)
        ret.columns = columns
        return ret

    def __setitem__(self, key, value):
        assert len(value) == len(self), 'new series is not of same length as df'
        if key not in self.columns:
            self.columns.append(key)
        if isinstance(value, Srs):
            value = value.values
        self.data[key] = Srs(value, name=key, index=self.index)
        pass

    def iterrows(self):
        collection = [self.index.values.data] + [self.data[col].values for col in self.columns]
        return zip(*collection)

    def itercols(self):
        for col in self.columns:
            yield self.data[col]

    def __getattr__(self, item):
        if item in self.columns:
            return self[:, item]
        new_data = {}
        for col in self.columns:
            new_data[col] = getattr(self.data[col], item)
        return partial(self.dict_apply, new_data)

    def dict_apply(self, func_dict):
        ret = {}
        for k, v in self.columns:
            try:
                ret[k] = [func_dict[k]()]
            except:
                pass
        return DF(ret)


if __name__ == '__main__':
    data = DF({'a': [10, 22, 32, 42, 25],
               'b': [100, 200, 200, 100, 300],
               'c': list('deanl')}, index=Idx(list('tbils')))
    df = data
    d = df.a + df.b
    df['d'] = d
    f = df.sum
    f()
    print(data)
    for i in data.itercols():
        print(i)
    data[:, 'c']
    data[[1, 4], ['b', 'c']]
    print()
    for i in zip((1, 3), (2, 3)): print(i)
