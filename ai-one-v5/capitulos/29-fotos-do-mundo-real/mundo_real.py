from collections import Counter

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import TensorDataset

from folha.conjunto import Folhas
from folha.emprestada import extrai, extratora, treina_cabeca
from folha.qualidade import confere, estraga, nao_folha
from folha.qualidade import tensores
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
s = np.random.default_rng(29)
valid = Folhas("validacao")
fotos = valid.imagens.permute(0, 2, 3, 1).numpy()     # N×H×W×C
y = valid.rotulos
grupos = {"normais": list(fotos)}
for tipo in ("escura", "flash", "borrada", "dedo"):
    grupos[tipo] = [estraga(f, tipo, s) for f in fotos]
grupos["não folha"] = [nao_folha(s, t) for t in ["chão"] * 100
                       + ["borrão"] * 100]

xt, yt = torch.load("caracteristicas.pt")["treino"]
cabeca = treina_cabeca(xt, yt)
resnet = extratora()
treino_norm = torch.nn.functional.normalize(xt, dim=1)
print("fotos       acerto  recusadas  nas aceitas  motivos")
notas = {}
for nome, lista in grupos.items():
    rotulos = torch.zeros(len(lista), dtype=torch.long)
    dados = TensorDataset(tensores(lista), rotulos)
    f, _ = extrai(resnet, dados)
    with torch.no_grad():
        p = cabeca(f).softmax(dim=1)
    unit = torch.nn.functional.normalize(f, dim=1)
    vizinho = (unit @ treino_norm.T).max(dim=1).values
    notas[nome] = (p.max(dim=1).values, vizinho)
    motivos = [confere(foto) for foto in lista]
    aceita = torch.tensor([m is None for m in motivos])
    recusa = 1 - aceita.float().mean()
    contagem = Counter(m for m in motivos if m)
    texto = ", ".join(f"{m} {n}"
                      for m, n in contagem.most_common(2))
    acerto = nas = "-"
    if nome != "não folha":
        certo = (p.argmax(dim=1) == y).float()
        acerto = f"{certo.mean():.1%}"
        if aceita.any():
            nas = f"{certo[aceita].mean():.1%}"
    print(f"{nome:10} {acerto:>7} {recusa:10.0%} {nas:>12}"
          f"  {texto}")

print("\nseparar 'não folha' das normais (AUROC):")
for i, nome in enumerate(("confiança da cabeça",
                          "semelhança com o treino")):
    normal = notas["normais"][i]
    estranha = notas["não folha"][i]
    rotulo = np.r_[np.ones(len(normal)),
                   np.zeros(len(estranha))]
    nota = torch.cat([normal, estranha]).numpy()
    print(f"  {nome:24} {roc_auc_score(rotulo, nota):.3f}")

limiar = notas["normais"][1].quantile(0.01)       # aceita 99%
pegas = (notas["não folha"][1] < limiar).float().mean()
print(f"\nlimiar que aceita 99% das normais: {limiar:.3f};")
print(f"com ele, a semelhança recusa {pegas:.0%}"
      " das sem folha")
