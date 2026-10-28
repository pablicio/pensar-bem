import torch
from torch import nn

from lauber.acervo import FAMILIAS, carrega, grade, partes
from lauber.classificador import Classificador, treina
from lauber.gan import treina_gan

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina(juiz, imgs[treino], familia[treino])
planas = imgs[treino].flatten(1)


def acervo(n):
    return planas[torch.randint(len(planas), (n,))]


torch.manual_seed(0)
gerador = nn.Sequential(nn.Linear(64, 256), nn.ReLU(),
                        nn.Linear(256, 3 * 32 * 32),
                        nn.Sigmoid())
perito = nn.Sequential(nn.Linear(3 * 32 * 32, 256),
                       nn.LeakyReLU(0.2), nn.Linear(256, 1))
fotos = treina_gan(gerador, perito, acervo, 3000, codigo=64,
                   lote=128, fotos=(3000,))
amostras = fotos[3000][0].view(-1, 3, 32, 32)
vistas = torch.bincount(juiz(amostras).argmax(1), minlength=6)
print("o juiz vê:")
for nome, quantas in zip(FAMILIAS, vistas.tolist()):
    print(f"  {nome:11} {quantas:5d}")
grade(amostras[:8], "densa.png", colunas=8)
