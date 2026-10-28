import torch

from folha.custo import multiplicacoes, parametros
from folha.redes import Inception

# o bloco "3a" da GoogLeNet: 192 canais de 28 × 28 na entrada
x = torch.zeros(1, 192, 28, 28)
print(f"{'':14} {'parâmetros':>11} {'multiplicações':>15}"
      f" {'saída':>16}")
versoes = [("sem gargalo", False), ("com gargalo", True)]
for nome, gargalo in versoes:
    bloco = Inception(192, 64, 96, 128, 16, 32, 32, gargalo)
    saida = tuple(bloco(x).shape[1:])
    print(f"{nome:14} {parametros(bloco):11,}"
          f" {multiplicacoes(bloco, x):15,} {str(saida):>16}")
