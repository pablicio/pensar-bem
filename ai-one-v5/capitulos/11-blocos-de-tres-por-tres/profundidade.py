import torch
from torch import nn

from folha.conjunto import Folhas
from folha.custo import multiplicacoes, parametros
from folha.redes import vgg
from folha.treino import acuracia, fixar_semente, lotes
from folha.treino import treinar_epoca

treino, valid = Folhas("treino"), Folhas("validacao")
x = torch.zeros(1, 3, 128, 128)
print(f"{'convoluções':>11} {'parâmetros':>11}"
      f" {'multiplic.':>12} {'perda':>6} {'validação':>9}")
for n in (1, 2, 3):
    fixar_semente(0, nucleos=4)
    rede = vgg(n)
    otimizador = torch.optim.Adam(rede.parameters(), lr=1e-3)
    carregador = lotes(treino, 64, semente=1)
    for epoca in range(10):
        perda = treinar_epoca(rede, carregador, otimizador,
                              nn.CrossEntropyLoss())
    print(f"{4 * n:11} {parametros(rede):11,}"
          f" {multiplicacoes(rede, x):12,} {perda:6.3f}"
          f" {acuracia(rede, lotes(valid, 256)):9.1%}")
