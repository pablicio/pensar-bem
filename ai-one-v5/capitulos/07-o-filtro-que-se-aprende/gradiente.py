import numpy as np
import torch
import torch.nn.functional as F

from folha.convolucao import correlaciona, gradientes

sorteio = np.random.default_rng(0)
x = sorteio.normal(size=(6, 6))
k = sorteio.normal(size=(3, 3))
g = sorteio.normal(size=(4, 4))         # dL/dY, sorteado

d_nucleo, d_entrada = gradientes(x, k, g)

xt = torch.tensor(x, requires_grad=True)
kt = torch.tensor(k, requires_grad=True)
y = F.conv2d(xt[None, None], kt[None, None])[0, 0]
(y * torch.tensor(g)).sum().backward()   # L = soma de Y · g

print("Y à mão = Y do PyTorch:",
      np.allclose(correlaciona(x, k), y.detach().numpy()))
print(f"dL/dK: {d_nucleo.shape}, diferença"
      f" {np.abs(d_nucleo - kt.grad.numpy()).max():.1e}")
print(f"dL/dX: {d_entrada.shape}, diferença"
      f" {np.abs(d_entrada - xt.grad.numpy()).max():.1e}")
