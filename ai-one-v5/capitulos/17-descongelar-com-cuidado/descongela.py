import matplotlib.pyplot as plt
import torch
from torch import nn

from folha.ajuste import montar, por_camadas, sonda
from folha.conjunto import Folhas
from folha.treino import acuracia, fixar_semente, lotes

treino, valid = Folhas("treino"), Folhas("validacao")
MARCAS = (1, 2, 3, 5, 8, 12, 20, 30)
ESTRATEGIAS = {
    "tudo, lr 1e-3": lambda r: [{"params": r.parameters(),
                                 "lr": 1e-3}],
    "tudo, lr 1e-4": lambda r: [{"params": r.parameters(),
                                 "lr": 1e-4}],
    "por camadas": lambda r: por_camadas(
        r, (1e-5, 3e-5, 1e-4, 3e-4, 1e-3)),
}
fixar_semente(0, nucleos=4)
rede = montar()
inicio = acuracia(rede, lotes(valid, 256))
print("estratégia      1 lote  5 lotes  3 épocas  dígitos")
print(f"congelada     {'-':>8} {'-':>8} {inicio:9.1%}"
      f" {sonda(rede[1]):8.1%}")
fig, ax = plt.subplots(figsize=(6, 3.4))
for nome, grupos in ESTRATEGIAS.items():
    fixar_semente(0, nucleos=4)
    rede = montar()
    otimizador = torch.optim.Adam(grupos(rede[1]))
    curva, lote = [inicio], 0
    for epoca in range(3):
        for x, y in lotes(treino, 64, semente=1 + epoca):
            rede.train()
            otimizador.zero_grad()
            nn.functional.cross_entropy(rede(x), y).backward()
            otimizador.step()
            lote += 1
            if lote in MARCAS:
                curva.append(acuracia(rede, lotes(valid, 256)))
    fim = acuracia(rede, lotes(valid, 256))
    um, cinco = curva[1], curva[4]
    print(f"{nome:13} {um:8.1%} {cinco:8.1%} {fim:9.1%}"
          f" {sonda(rede[1]):8.1%}")
    ax.plot((0, *MARCAS), curva, marker="o", label=nome)
ax.axhline(inicio, color="gray", ls="--", label="congelada")
ax.set_xlabel("lotes de ajuste")
ax.set_ylabel("acerto na validação")
ax.legend()
fig.tight_layout()
fig.savefig("primeiros_lotes.png", dpi=300)
