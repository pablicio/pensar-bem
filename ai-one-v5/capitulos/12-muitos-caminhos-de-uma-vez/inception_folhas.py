import csv

import numpy as np
import torch
from torch import nn

from folha.conjunto import PASTA, Folhas
from folha.custo import multiplicacoes, parametros
from folha.redes import rede_inception, vgg
from folha.treino import fixar_semente, lotes, prever
from folha.treino import treinar_epoca

treino, valid = Folhas("treino"), Folhas("validacao")

# o tamanho típico das lesões de cada foto, em pixels de 128
lados = {}
with open(PASTA / "caixas.csv", encoding="utf-8") as f:
    for c in csv.DictReader(f):
        lado = min(int(c["x1"]) - int(c["x0"]),
                   int(c["y1"]) - int(c["y0"])) / 2
        lados.setdefault(c["foto"], []).append(lado)
tamanho = np.array([np.median(lados.get(f["foto"], [np.nan]))
                    for f in valid.linhas])
limites = np.nanquantile(tamanho, [1 / 3, 2 / 3])
faixas = {"pequenas": tamanho <= limites[0],
          "médias": (tamanho > limites[0])
          & (tamanho <= limites[1]),
          "grandes": tamanho > limites[1]}
print(f"lesões pequenas: até {limites[0]:.1f} pixels;"
      f" grandes: acima de {limites[1]:.1f}")

x = torch.zeros(1, 3, 128, 128)
print(f"{'':10} {'parâm.':>7} {'mult.':>6} {'valid.':>7}"
      + "".join(f" {k:>8}" for k in faixas))
for nome, construtor in [("VGG", lambda: vgg(1)),
                         ("Inception", rede_inception)]:
    fixar_semente(0, nucleos=4)
    rede = construtor()
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    for epoca in range(10):
        treinar_epoca(rede, carregador, otimizador,
                      nn.CrossEntropyLoss())
    previstas, certas = prever(rede, lotes(valid, 256))
    certo = (previstas == certas).numpy()
    mult = multiplicacoes(rede, x) / 1e6          # em milhões
    print(f"{nome:10} {parametros(rede):7,} {mult:6.1f}"
          f" {certo.mean():7.1%}"
          + "".join(f" {certo[m].mean():8.1%}"
                    for m in faixas.values()))
