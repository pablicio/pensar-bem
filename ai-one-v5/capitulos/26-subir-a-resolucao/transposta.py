import numpy as np
import torch
from torch.nn import functional as F

from folha.transposta import tamanho_transposta, toeplitz_passo

nucleo = np.array([[1.0, 2, 0], [0, 1, -1], [3, 0, 1]])
w = torch.tensor(nucleo)[None, None]
n, passo = 5, 2
T = toeplitz_passo(nucleo, n, passo)
print("T:", T.shape, "— a convolução leva 5 × 5 a 2 × 2")

x = np.arange(25.0).reshape(5, 5)
ida = (T @ x.ravel()).reshape(2, 2)
pronto = F.conv2d(torch.tensor(x)[None, None], w, stride=passo)
print("ida pela matriz igual à conv2d:",
      np.allclose(ida, pronto[0, 0].numpy()))

z = np.array([[1.0, 2], [3, 4]])
volta = (T.T @ z.ravel()).reshape(5, 5)
transposta = F.conv_transpose2d(torch.tensor(z)[None, None], w,
                                stride=passo)
print("volta pela transposta:")
print(volta)
print("igual à conv_transpose2d:",
      np.allclose(volta, transposta[0, 0].numpy()))
print("lado da saída pela fórmula:",
      tamanho_transposta(2, 3, 2))
