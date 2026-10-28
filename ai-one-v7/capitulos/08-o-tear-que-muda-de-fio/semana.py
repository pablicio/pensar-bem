import matplotlib.pyplot as plt
import numpy as np
import torch

from dados.gerar_malha import defeito, malha
from lauber.anomalia import (Malha, carrega_malha, escores,
                             mapa_de_erro)

# a semana do tear 14: um quadro por minuto e as trocas de fio
TROCAS = [(0, "preta"), (2 * 1440, "mescla"),
          (4 * 1440, "azul"), (5 * 1440 + 600, "mescla")]
MINUTOS, CALIBRA = 7 * 1440, 40
sorteio = np.random.default_rng(14)
artigo = np.empty(MINUTOS, dtype=object)
for inicio, nome in TROCAS:
    artigo[inicio:] = nome
furo = np.zeros(MINUTOS, bool)
furo[sorteio.choice(MINUTOS, size=12, replace=False)] = True
fotos = []
for m in range(MINUTOS):
    img = malha(sorteio, artigo[m])
    if furo[m]:
        img, _ = defeito(sorteio, img, "furo")
    fotos.append(np.clip(img, 0, 1))
fotos = torch.tensor(np.array(fotos), dtype=torch.float32)
rede = Malha()
rede.load_state_dict(torch.load("malha.pt"))
escore = escores(mapa_de_erro(rede, fotos[:, None]))[1].numpy()
# 1. o limiar do capítulo 6: 1% das fotos boas do teste
_, teste, info = carrega_malha()
local = escores(mapa_de_erro(rede, teste))[1].numpy()
unico = np.quantile(local[info["tipo_teste"] == "bom"], 0.99)
# 2. um limiar por troca: o maior escore dos 40 primeiros
# minutos do fio novo, com 20% de folga
por_troca = np.empty(MINUTOS)
for inicio, nome in TROCAS:
    calibra = escore[inicio:inicio + CALIBRA]
    por_troca[inicio:] = 1.2 * calibra.max()
print("                  alarmes falsos           furos")
print("                  preta   azul  mescla  achados")
for nome, limiar in (("limiar único", unico),
                     ("limiar por troca", por_troca)):
    alarme = escore > limiar
    falsos = [(alarme & ~furo & (artigo == a)).sum()
              for a in ("preta", "azul", "mescla")]
    print(f"{nome:16}", " ".join(f"{f:6d}" for f in falsos),
          f"{(alarme & furo).sum():6d} de {furo.sum()}")
horas = np.arange(MINUTOS) / 60
fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(horas, escore, lw=0.3, color="#555")
ax.plot(horas[furo], escore[furo], "o", color="#c33",
        ms=4, label="furo")
ax.axhline(unico, color="#36a", ls=":", label="limiar único")
ax.plot(horas, por_troca, color="#a70",
        label="limiar por troca")
ax.set_yscale("log")
ax.set_xlabel("horas da semana")
ax.set_ylabel("maior erro local")
ax.legend(fontsize=7, loc="upper left")
fig.tight_layout()
fig.savefig("semana.png", dpi=300)
