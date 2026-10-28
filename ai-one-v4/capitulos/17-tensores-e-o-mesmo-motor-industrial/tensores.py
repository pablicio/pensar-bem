import numpy as np
import torch

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(a.dtype, a.shape, a.device)
print(a @ a)                          # o mesmo @ do NumPy
print(a.sum(dim=0), a.mean())         # dim no lugar de axis

x = np.arange(4.0)
t = torch.from_numpy(x)               # divide a memória
t[0] = 99.0
print(x, t.dtype)
