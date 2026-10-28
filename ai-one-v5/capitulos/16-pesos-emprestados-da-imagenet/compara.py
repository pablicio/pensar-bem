import torch
from torch import nn

from folha.conjunto import CLASSES, Folhas
from folha.emprestada import treina_cabeca
from folha.redes import rede_global
from folha.treino import fixar_semente, lotes, prever
from folha.treino import treinar_epoca

BICHO = CLASSES.index("bicho-mineiro")


def linha(nome, prevista, certa):
    total = (prevista == certa).float().mean()
    bicho = (prevista[certa == BICHO] == BICHO).float().mean()
    print(f"{nome:26} {total:7.1%} {bicho:9.0%}")


print("rede                       acerto  bicho-min.")
fixar_semente(0, nucleos=4)
rede = rede_global()
otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
carregador = lotes(Folhas("treino"), 64, semente=1)
for _ in range(10):
    treinar_epoca(rede, carregador, otimizador,
                  nn.CrossEntropyLoss())
linha("do zero, 10 épocas", *prever(rede, lotes(
    Folhas("validacao"), 256)))

matrizes = torch.load("caracteristicas.pt")
xt, yt = matrizes["treino"]
xv, yv = matrizes["validacao"]
cabeca = treina_cabeca(xt, yt)
linha("ResNet-18 + cabeça nova", cabeca(xv).argmax(dim=1), yv)
print("parâmetros treinados na cabeça:",
      sum(p.numel() for p in cabeca.parameters()))
