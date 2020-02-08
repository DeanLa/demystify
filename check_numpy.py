from functools import partial

import numpy as np
from numpy.lib.stride_tricks import as_strided
x = np.arange(10)#.reshape(10,1)
y = np.arange(20).reshape(10,2)
z = np.broadcast_to(x,(10,2))

np.lib.stride_tricks
def add(x,y,z):
    return x+y+z

add5 = partial(add, z=5)
add5(3,4)
