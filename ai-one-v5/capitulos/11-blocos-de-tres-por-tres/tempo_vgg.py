import time

import torch

from folha.redes import vgg

torch.set_num_threads(4)
x = torch.zeros(1, 3, 128, 128)
for n in (1, 2, 3):
    rede = vgg(n).eval()
    with torch.no_grad():
        rede(x)                  # a primeira é mais lenta
        tempos = []
        for _ in range(20):
            inicio = time.perf_counter()
            rede(x)
            tempos.append(time.perf_counter() - inicio)
    ms = min(tempos) * 1000
    print(f"{4 * n:2} convoluções: {ms:5.1f} ms por foto")
