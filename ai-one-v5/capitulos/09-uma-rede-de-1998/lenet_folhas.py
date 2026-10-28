import torch
import torch.nn.functional as F
from torch import nn

from folha.conjunto import Folhas
from folha.redes import lenet
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca


def reduzidas(parte):
    """As fotos da parte, reduzidas a 32 × 32 pela média."""
    dados = Folhas(parte)
    x = dados.imagens.float()
    x = F.interpolate(x, size=32, mode="area")
    dados.imagens = x.round().to(torch.uint8)
    return dados


fixar_semente(0)
treino, valid = reduzidas("treino"), reduzidas("validacao")
rede = lenet(canais=3, classes=6)
otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
carregador = lotes(treino, 64, semente=1)
for epoca in range(1, 31):
    treinar_epoca(rede, carregador, otimizador,
                  nn.CrossEntropyLoss())
    if epoca % 10 == 0:
        acerto = acuracia(rede, lotes(valid, 256))
        print(f"época {epoca:2}: validação {acerto:.1%}")
