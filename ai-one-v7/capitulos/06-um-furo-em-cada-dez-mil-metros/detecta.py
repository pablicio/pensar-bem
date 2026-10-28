import time

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import roc_auc_score, roc_curve

from lauber.anomalia import (Malha, carrega_malha, escores,
                             mapa_de_erro)
from lauber.autoencoder import treina

DEFEITOS = ["furo", "agulha", "mancha"]
CORES = {"bom": "#888", "furo": "#c33", "agulha": "#36a",
         "mancha": "#a70"}
torch.manual_seed(0)
treino, teste, info = carrega_malha()
tipo = info["tipo_teste"]
print(f"treino: {len(treino)} fotos boas; teste:"
      f" {(tipo == 'bom').sum()} boas e"
      f" {(tipo != 'bom').sum()} com defeito")
rede = Malha()
inicio = time.time()
treina(rede, treino, epocas=10)
print(f"{time.time() - inicio:.0f} s de treino")
torch.save(rede.state_dict(), "malha.pt")
mapa = mapa_de_erro(rede, teste)
media, local = (e.numpy() for e in escores(mapa))
print("área sob a curva ROC   furo  agulha  mancha")
for nome, e in (("erro médio", media),
                ("maior erro local", local)):
    aucs = []
    for d in DEFEITOS:
        s = (tipo == "bom") | (tipo == d)
        aucs.append(roc_auc_score(tipo[s] == d, e[s]))
    print(f"{nome:20}", " ".join(f"{a:7.3f}" for a in aucs))
# o limiar que dispara em 1% das fotos boas
limiar = np.quantile(local[tipo == "bom"], 0.99)
print(f"limiar com 1% de alarme falso: {limiar:.4f}")
artigo = info["artigo_teste"]
print("achados       preta   azul  branca  todas")
for d in DEFEITOS:
    taxas = [np.mean(local[(tipo == d) & (artigo == a)]
                     > limiar)
             for a in ("preta", "azul", "branca")]
    taxas.append(np.mean(local[tipo == d] > limiar))
    print(f"  {d:8}", " ".join(f"{t:6.0%}" for t in taxas))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3))
for d in ["bom"] + DEFEITOS:
    a1.hist(np.log10(local[tipo == d]), bins=40, density=True,
            alpha=0.5, label=d, color=CORES[d])
    if d != "bom":
        s = (tipo == "bom") | (tipo == d)
        fp, vp, _ = roc_curve(tipo[s] == d, local[s])
        a2.plot(fp, vp, label=d, color=CORES[d])
a1.axvline(np.log10(limiar), color="k", ls=":")
a1.set_xlabel("log10 do maior erro local")
a1.legend(fontsize=7)
a2.plot([0, 1], [0, 1], "k:", lw=0.8)
a2.set_xlabel("falsos alarmes")
a2.set_ylabel("defeitos achados")
a2.legend(fontsize=7)
fig.tight_layout()
fig.savefig("roc.png", dpi=300)
