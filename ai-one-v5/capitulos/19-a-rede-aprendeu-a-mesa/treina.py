import torch
from torch import nn
from torchvision.transforms import v2

from folha.conjunto import Folhas
from folha.fundos import FundoTrocado
from folha.redes import rede_global
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

MATIZ = v2.ColorJitter(hue=0.5)
REDES = [("sempre", Folhas("treino")),
         ("matiz", Folhas("treino", transforma=MATIZ)),
         ("matiz_fundos",
          FundoTrocado("treino", transforma=MATIZ))]
valid = Folhas("validacao")
for nome, treino in REDES:
    fixar_semente(0, nucleos=4)
    rede = rede_global()
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    for _ in range(30):
        treinar_epoca(rede, carregador, otimizador,
                      nn.CrossEntropyLoss())
    acerto = acuracia(rede, lotes(valid, 256))
    print(f"{nome:13} validação {acerto:.1%}")
    torch.save(rede.state_dict(), f"{nome}.pt")
