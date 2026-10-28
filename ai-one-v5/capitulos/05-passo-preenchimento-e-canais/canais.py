import numpy as np
import torch
import torch.nn.functional as F

from folha.conjunto import abre
from folha.convolucao import conv2d

x = abre(1).transpose(2, 0, 1) / 255          # (3, 128, 128)
sorteio = np.random.default_rng(0)
w = sorteio.normal(size=(4, 3, 3, 3))    # 4 núcleos 3×3×3
b = sorteio.normal(size=4)

for passo, preenche in [(1, 0), (1, 1), (2, 1)]:
    meu = conv2d(x, w, b, passo, preenche)
    torch_ = F.conv2d(torch.tensor(x)[None], torch.tensor(w),
                      torch.tensor(b), stride=passo,
                      padding=preenche)[0].numpy()
    dif = np.abs(meu - torch_).max()
    print(f"passo {passo}, preenchimento {preenche}:"
          f" saída {meu.shape}, diferença {dif:.1e}")
