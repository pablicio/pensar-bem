import torch
from torch import nn
from torchvision.transforms import v2

from folha.conjunto import CLASSES, Folhas
from folha.redes import rede_global
from folha.treino import fixar_semente, lotes, prever
from folha.treino import treinar_epoca

SADIA, FERRUGEM, SOL = (CLASSES.index(c)
                        for c in ("sadia", "ferrugem", "sol"))
AUMENTOS = [("luz", v2.ColorJitter(0.3, 0.3, 0.2, 0.02), None),
            ("matiz", v2.ColorJitter(hue=0.5), None),
            ("cinza", v2.Grayscale(3), v2.Grayscale(3))]
print("aumento  validação  ferrugem  sol  sol → sadia")
for nome, no_treino, na_validacao in AUMENTOS:
    treino = Folhas("treino", transforma=no_treino)
    valid = Folhas("validacao", transforma=na_validacao)
    fixar_semente(0, nucleos=4)
    rede = rede_global()
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    for _ in range(30):
        treinar_epoca(rede, carregador, otimizador,
                      nn.CrossEntropyLoss())
    prevista, certa = prever(rede, lotes(valid, 256))
    acerto = (prevista == certa).float()
    ferrugem = acerto[certa == FERRUGEM].mean()
    sol = acerto[certa == SOL].mean()
    trocas = ((certa == SOL) & (prevista == SADIA)).sum()
    print(f"{nome:7} {acerto.mean():10.1%} {ferrugem:9.0%}"
          f" {sol:4.0%} {trocas:5} de {(certa == SOL).sum()}")
