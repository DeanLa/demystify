from functools import partial

import numpy as np
x = np.arange(10)
y = np.arange(20).reshape(10,2)
x = np.broadcast(x,y)
def add(x,y,z):
    return x+y+z

add5 = partial(add, z=5)
add5(3,4)