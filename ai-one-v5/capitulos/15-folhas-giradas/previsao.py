import torch

from folha.giradas import Giradas
from folha.redes import rede_global
from folha.treino import lotes

rede = rede_global()
rede.load_state_dict(torch.load("sem.pt"))
rede.eval()


@torch.no_grad()
def oito_vezes(x):
    """A média das probabilidades nas 8 simetrias."""
    soma = 0
    for espelho in (x, x.flip(3)):
        for k in range(4):         # 0, 90, 180 e 270 graus
            girada = torch.rot90(espelho, k, dims=(2, 3))
            soma = soma + torch.softmax(rede(girada), dim=1)
    return soma / 8


for qual in ("em_pe", "girada"):
    dados = Giradas(qual)
    uma = oito = 0
    for x, y in lotes(dados, 100):
        with torch.no_grad():
            uma += (rede(x).argmax(dim=1) == y).sum().item()
        oito += (oito_vezes(x).argmax(dim=1) == y).sum().item()
    print(f"{qual:6}  uma passada: {uma / len(dados):.1%}"
          f"  oito passadas: {oito / len(dados):.1%}")
