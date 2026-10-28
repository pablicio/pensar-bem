import time

import torch
import torch.nn.functional as F

from lupa.escaneado import conjunto
from lupa.vit import CNN, ViT

torch.set_num_threads(4)
x_teste, y_teste = conjunto(2000, semente=1)


def treina(modelo, x, y, passos=600, B=64):
    opt = torch.optim.AdamW(modelo.parameters(), lr=1e-3)
    g = torch.Generator().manual_seed(0)
    modelo.train()
    for _ in range(passos):
        i = torch.randint(0, len(y), (B,), generator=g)
        perda = F.cross_entropy(modelo(x[i]), y[i])
        opt.zero_grad()
        perda.backward()
        opt.step()
    modelo.eval()
    with torch.no_grad():
        acerto = (modelo(x_teste).argmax(1) == y_teste)
    return acerto.float().mean().item()


for n, passos in [(500, 600), (5000, 600), (20000, 2000)]:
    x, y = conjunto(n, semente=0)
    for nome, fabrica in [("CNN", CNN), ("ViT", ViT)]:
        torch.manual_seed(0)
        modelo = fabrica()
        params = sum(p.numel() for p in modelo.parameters())
        inicio = time.time()
        acerto = treina(modelo, x, y, passos)
        segundos = time.time() - inicio
        print(f"{n:5} imagens, {nome}: {params:6} parâmetros,"
              f" acerto {acerto:.3f} ({segundos:.0f} s)")
