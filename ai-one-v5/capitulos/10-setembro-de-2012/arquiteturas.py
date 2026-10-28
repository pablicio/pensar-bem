import torch
from torch import nn
from torchvision import models

from folha.custo import multiplicacoes, parametros
from folha.redes import lenet

REDES = [("LeNet-5", 1998, lenet(), 32, 1),
         ("AlexNet", 2012, models.alexnet(), 224, 3),
         ("VGG-16", 2014, models.vgg16(), 224, 3),
         ("ResNet-18", 2015, models.resnet18(), 224, 3)]
print(f"{'rede':10} {'ano':>4} {'entrada':>8}"
      f" {'parâmetros':>12} {'multiplicações':>15}")
for nome, ano, rede, lado, canais in REDES:
    x = torch.zeros(1, canais, lado, lado)
    mult = multiplicacoes(rede, x)
    print(f"{nome:10} {ano:4} {lado:>5}×{lado:<3}"
          f" {parametros(rede):12,} {mult:15,}")

print()
print("as camadas convolucionais da AlexNet:")
x = torch.zeros(1, 3, 224, 224)
for camada in models.alexnet().features:
    x = camada(x)
    if isinstance(camada, (nn.Conv2d, nn.MaxPool2d)):
        k = camada.kernel_size
        k = k[0] if isinstance(k, tuple) else k
        s = camada.stride
        s = s[0] if isinstance(s, tuple) else s
        tipo = type(camada).__name__
        print(f"  {tipo:10} {k:2}×{k:<2} passo {s}"
              f"  →  {tuple(x.shape[1:])}")
