import numpy as np


def softmax_ingenua(z):
    e = np.exp(z)
    return e / e.sum()


print(softmax_ingenua(np.array([2.0, 1.0, 0.1])).round(3))
with np.errstate(over="ignore", invalid="ignore"):
    print("exp(1000) =", np.exp(1000.0))
    print(softmax_ingenua(np.array([1000.0, 999.0, 998.0])))
