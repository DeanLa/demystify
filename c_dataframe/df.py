from functools import partial

from a_array.array import Arr
from b_series.s1 import Idx, Srs


class DF:
    def __init__(self, data, index=None):
        self.columns = list(data.keys()) # Changed
        self.data = data
        self.index = index
        self._validate()
        for name in self.columns:
            self[name] = data[name] # Uses its own __setitem__

    def _validate(self):
        for col in self.data.values():
            assert len(col) == len(self), f"Not all columns are of same length {self.shape}, {len(col)}"
        self.index = self.index or Idx(range(len(self)))  # In real code, this will not be in validate.
        assert len(self.index)

    @property # Uses property
    def shape(self):
        return (len(self.data[self.columns[0]]),len(self.columns))

    def __len__(self):
        return self.shape[0]

    def __iter__(self):
        collection = [self.index.values.data] + [self.data[col].values for col in self.columns]
        return zip(*collection)

    def __str__(self):
        maxlen = max([len(col_name) for col_name in self.columns]) + 2  # Will make for nice spaces
        maxlen = max(maxlen, 8)
        ret = ''.center(maxlen)  # Top-Left Corner
        ret += spaced_row(self.columns, maxlen)
        for row in self:  # This part changes
            ret += spaced_row(row, maxlen)
        return ret

    __repr__ = __str__

    def _repr_markdown_(self):
        ret = '|'  # Top-Left Corner
        ret += markdown_row(self.columns)
        # the --- row
        ret += markdown_row(['---'] * (self.shape[1] + 1))
        for row in self:  # This part changes
            ret += markdown_row(row)
        return ret

    def __setitem__(self, key, value):
        assert len(value) == len(self), 'new series is not of same length as df'
        if key not in self.columns:  # If it is in the columns, it just replaces the current
            self.columns.append(key)  # This will change the shape
        if isinstance(value, Srs):  # We did this in __init__. Remember?
            value = value.values
        self.data[key] = Srs(value, name=key, index=self.index)

    def __getitem__(self, items):
        if not isinstance(items, tuple):
            items = (items,)
        if len(items) == 1:
            # Bring all rows
            return self[:, items[0]]
        rowidx, colidx = items
        if colidx == slice(None):
            columns = self.columns
        elif isinstance(colidx, str):
            # Just return the series
            s = self.data[colidx]
            return s[rowidx]
        else:
            # Take relevant columns
            columns = [col for col in self.columns if col in colidx]  # Do we have to create a new dataframe?
        data = {col: self.data[col][rowidx] for col in columns}
        index = data[columns[0]].index
        ret = DF(data, index=index)
        return ret

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
        for col in self.columns:
            try:
                ret[col] = [func_dict[col]()]
            except:
                pass
        return DF(ret)


def spaced_row(row, maxlen):
    ret = ''
    for cell in row:
        ret += str(cell).center(maxlen)
    ret += '\n'
    return ret


def markdown_row(row):
    ret = ''
    for cell in row:
        ret += '| ' + str(cell)
    ret += '|\n'
    return ret


if __name__ == '__main__':
    data = {'flights': [10, 12, 50, 40],
            'size': [1, 2, 5, 4],
            'country': ['Israel', 'Georgia', 'US', 'US']}
    index = Idx(['tlv', 'tbs', 'jfk', 'ewr'])
    df = DF(data, index)
    df['mayor'] = ['Huldai', 'Kaladze', 'De Blasio', 'Baraka']
    df
