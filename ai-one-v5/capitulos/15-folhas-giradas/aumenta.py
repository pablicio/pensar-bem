import torch
from torch import nn
from torchvision.transforms import v2

from folha.conjunto import Folhas
from folha.giradas import Giradas
from folha.redes import rede_global
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

GIRA = v2.Compose([v2.RandomHorizontalFlip(),
                   v2.RandomRotation(180)])
valid = Folhas("validacao")
em_pe, girada = Giradas("em_pe"), Giradas("girada")
print("treino       épocas  validação  em pé  girada")
for nome, transforma in [("sem aumento", None),
                         ("com rotação", GIRA)]:
    treino = Folhas("treino", transforma=transforma)
    fixar_semente(0, nucleos=4)
    rede = rede_global()
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    for epoca in range(1, 31):
        treinar_epoca(rede, carregador, otimizador,
                      nn.CrossEntropyLoss())
        if epoca in (10, 30):
            a, b, c = (acuracia(rede, lotes(d, 256))
                       for d in (valid, em_pe, girada))
            print(f"{nome:12} {epoca:6} {a:10.1%} {b:6.1%}"
                  f" {c:7.1%}")
    torch.save(rede.state_dict(), f"{nome.split()[0]}.pt")
