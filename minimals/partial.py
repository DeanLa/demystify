from functools import partial


def add(x, y):
    return x + 10 * y


print(add(5, 1))

add5 = partial(add, 5)
print(add5(1))
add100 = partial(add, y=10)
print(add100(5))

def func_runner(funcs):
    return [f() for f in funcs]

func_runner([add])
funcs = [
    partial(add,5,1),
    partial(add,1,5),
]
func_runner(funcs)