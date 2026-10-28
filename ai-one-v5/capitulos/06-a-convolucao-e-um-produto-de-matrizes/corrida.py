import time

import numpy as np
import torch
import torch.nn.functional as F

from folha.conjunto import abre
from folha.convolucao import conv2d, conv2d_matricial, im2col

x = abre(1).transpose(2, 0, 1) / 255        # (3, 128, 128)
sorteio = np.random.default_rng(0)
w = sorteio.normal(size=(16, 3, 3, 3))
b = sorteio.normal(size=16)


def mede(nome, funcao):
    """O melhor de cinco tempos, em milissegundos."""
    tempos = []
    for _ in range(5):
        inicio = time.perf_counter()
        y = funcao()
        tempos.append(time.perf_counter() - inicio)
    print(f"{nome:26} {min(tempos) * 1000:9.1f} ms")
    return y


laco = mede("laços (cap. 5)", lambda: conv2d(x, w, b, 1, 1))
cols = mede("im2col: montar as colunas",
            lambda: im2col(x, 3, 1, 1)[0])
mede("im2col: multiplicar",
     lambda: w.reshape(16, 27) @ cols + b[:, None])
mat = mede("im2col: tudo",
           lambda: conv2d_matricial(x, w, b, 1, 1))
xt, wt, bt = (torch.tensor(a, dtype=torch.float32)
              for a in (x, w, b))
pt = mede("F.conv2d do PyTorch",
          lambda: F.conv2d(xt[None], wt, bt, padding=1)[0])
for nome, outra in [("im2col", mat), ("PyTorch", pt.numpy())]:
    dif = np.abs(laco - outra).max()
    print(f"laços contra {nome}: diferença {dif:.1e}")
