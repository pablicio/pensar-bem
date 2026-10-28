import numpy as np

from perdas import softmax

print(softmax(np.array([2.0, 1.0, 0.1])).round(3))
print(softmax(np.array([1000.0, 999.0, 998.0])).round(3))
print(softmax(np.array([-1000.0, -999.0, -998.0])).round(3))
