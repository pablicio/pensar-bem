import torch
from torch import nn

from folha.conjunto import DESVIO, MEDIA, Folhas
from folha.resnet import resnet_pequena
from folha.treino import acuracia, fixar_semente, lotes

fixar_semente(0, nucleos=4)
treino, valid = Folhas("treino"), Folhas("validacao")
media = torch.tensor(MEDIA).view(1, 3, 1, 1)
desvio = torch.tensor(DESVIO).view(1, 3, 1, 1)


def escurece(x):
    """A foto com 35% da luz, normalizada de novo."""
    return ((x * desvio + media) * 0.35 - media) / desvio


def carrega():
    rede = resnet_pequena(3)
    rede.load_state_dict(torch.load("resnet_bn.pt"))
    return rede


@torch.no_grad()
def passa(rede, dados, muda=None, acumula=False):
    """Fotos no modo de treino: só as estatísticas mudam."""
    for camada in rede.modules():
        if acumula and isinstance(camada, nn.BatchNorm2d):
            camada.reset_running_stats()
            camada.momentum = None   # média simples dos lotes
    rede.train()
    for x, _ in lotes(dados, 64):
        rede(muda(x) if muda else x)


def mede(rede):
    return f"{acuracia(rede, lotes(valid, 256)):.1%}"


print("como saiu do treino:    ", mede(carrega()))
rede = carrega()
passa(rede, valid, muda=escurece)
print("depois de fotos escuras:", mede(rede))
rede = carrega()
passa(rede, treino, acumula=True)
print("reestimada no treino:   ", mede(rede))
