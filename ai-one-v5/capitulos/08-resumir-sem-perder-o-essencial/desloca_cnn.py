from pathlib import Path

import torch
from torch import nn

from folha.conjunto import Folhas
from folha.redes import rede_densa, rede_global
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

treino, valid = Folhas("treino"), Folhas("validacao")
originais = valid.imagens.clone()
DESLOCAMENTOS = [0, 1, 3, 5, 8, 16, 32]
cabecalho = "".join(f"{d:>7}" for d in DESLOCAMENTOS)
print(f"{'pixels':>14}{cabecalho}")
redes = [("densa no fim", rede_densa),
         ("média global", rede_global)]
for nome, construtor in redes:
    fixar_semente(0)
    rede = construtor()
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    for epoca in range(10):
        treinar_epoca(rede, carregador, otimizador,
                      nn.CrossEntropyLoss())
    linha = f"{nome:14}"
    for d in DESLOCAMENTOS:
        valid.imagens = torch.roll(originais, d, dims=3)
        linha += f"{acuracia(rede, lotes(valid, 256)):7.1%}"
    print(linha)
valid.imagens = originais
Path("modelos").mkdir(exist_ok=True)
torch.save(rede.state_dict(), "modelos/cnn_global.pt")
