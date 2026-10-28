import torch
from torchvision.transforms import v2

from folha.conjunto import Folhas
from folha.redes import rede_global
from folha.treino import acuracia, lotes

rede = rede_global()
rede.load_state_dict(torch.load("sem.pt"))
for angulo in (0, 45, 90, 180):
    def gira(x, a=angulo):
        return v2.functional.rotate(x, a)
    valid = Folhas("validacao", transforma=gira)
    print(f"validação girada {angulo:3}°:"
          f" {acuracia(rede, lotes(valid, 256)):.1%}")
