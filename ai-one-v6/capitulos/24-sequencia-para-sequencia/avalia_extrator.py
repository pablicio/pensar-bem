import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from rio.extrator import (CAMPOS, Extrator, confere, registro,
                          vocabularios)
from rio.leitor import preenche
from rio.texto import mensagens, parte

tab = mensagens()
pedidos = tab[tab["verdade"].isin(["risco", "ajuda"])]
treino = parte(pedidos, "treino")
teste = parte(pedidos, "teste")
registros = [registro(l) for _, l in treino.iterrows()]
entrada, saida = vocabularios(treino["texto"], registros)
modelo = Extrator(len(entrada), len(saida))
modelo.load_state_dict(torch.load("extrator.pt"))
x, n = preenche(entrada, teste["texto"], maximo=240)
gerado = modelo.extrai(x, n, saida)
textos = teste["texto"].tolist()
certo = [registro(l) for _, l in teste.iterrows()]
conferido, suspeito = zip(*(confere(g, t)
                            for g, t in zip(gerado, textos)))
suspeito = np.array(suspeito)


def campos(r):
    partes = r.split("|")
    return partes if len(partes) == 4 else [None] * 4


print(f"{len(teste)} pedidos de teste")
print("campo     rede  conferida")
for k, c in enumerate(CAMPOS):
    a = np.mean([campos(g)[k] == campos(r)[k]
                 for g, r in zip(gerado, certo)])
    b = np.mean([campos(g)[k] == campos(r)[k]
                 for g, r in zip(conferido, certo)])
    print(f"{c:8} {a:6.1%} {b:9.1%}")
exato = np.array([g == r for g, r in zip(gerado, certo)])
exato_c = np.array([g == r for g, r in zip(conferido, certo)])
print(f"registro {exato.mean():6.1%} {exato_c.mean():9.1%}")
inventado = sum(campos(g)[2] not in (None, "")
                and campos(g)[2] not in re.findall(r"\d+", t)
                for g, t in zip(gerado, textos))
print(f"números que não estão na mensagem: {inventado}")
for g, r in [(g, r) for g, r in zip(gerado, certo)
             if campos(g)[2] != campos(r)[2]][:4]:
    a, b = campos(g)[2], campos(r)[2]
    print(f"  escreveu {a:>5}, era {b:>5}")
FAIXAS = [(0, 60), (60, 100), (100, 140), (140, 240)]
tamanho = n.numpy()
print("caracteres  pedidos  registro exato (rede)")
taxas = []
for a, b in FAIXAS:
    s = (tamanho >= a) & (tamanho < b)
    taxas.append(exato[s].mean())
    print(f"{a:3d} a {b:3d} {s.sum():8d} {taxas[-1]:10.1%}")
fig, ax = plt.subplots(figsize=(6, 3))
ax.bar([f"{a}–{b}" for a, b in FAIXAS], taxas, color="#335")
ax.set_xlabel("caracteres na mensagem")
ax.set_ylabel("registros exatos")
fig.tight_layout()
fig.savefig("tamanho.png", dpi=300)
outros = exato_c[~suspeito].mean()
print(f"suspeitos: {suspeito.mean():.1%};"
      f" exatos entre os outros: {outros:.1%}")
ivone = textos.index(next(t for t in textos
                          if t.endswith("ivone")))
print("Dona Ivone:", gerado[ivone])
print("  conferido:", conferido[ivone],
      "(suspeito)" if suspeito[ivone] else "")
print("  certo:    ", certo[ivone])
