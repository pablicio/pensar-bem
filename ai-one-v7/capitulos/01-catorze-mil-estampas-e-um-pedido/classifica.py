import time

import torch

from lauber.acervo import carrega, partes
from lauber.classificador import Classificador, acerto, treina

torch.manual_seed(0)
imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, valid, teste = partes(len(imgs))
rede = Classificador()
inicio = time.time()
treina(rede, imgs[treino], familia[treino])
print(f"{time.time() - inicio:.0f} s de treino")
for nome, parte in [("validação", valid), ("teste", teste)]:
    taxa = acerto(rede, imgs[parte], familia[parte])
    print(f"acerto ({nome}): {taxa:.1%}")
torch.save(rede.state_dict(), "classificador.pt")
