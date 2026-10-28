import numpy as np

from ativacoes import relu

W1 = np.array([[1.0, 1.0], [1.0, 1.0]])
b1 = np.array([0.0, -1.0])
w2 = np.array([1.0, -2.0])

print("x1 x2   h1  h2   saída")
for x1, x2 in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    h = relu(W1 @ np.array([x1, x2]) + b1)
    s = w2 @ h
    print(f" {x1}  {x2}   {h[0]:.0f}   {h[1]:.0f}     {s:.0f}")
