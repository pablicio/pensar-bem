import torch

from folha.bolso import ESPINHAS, espinha
from folha.conjunto import Folhas
from folha.custo import multiplicacoes, parametros
from folha.emprestada import extrai, treina_cabeca
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
treino, valid = Folhas("treino"), Folhas("validacao")
foto = torch.zeros(1, 3, 128, 128)
print("espinha           parâmetros  MB (float32)"
      "  multiplic.  acerto")
for nome in ESPINHAS:
    rede, n = espinha(nome)
    xt, yt = extrai(rede, treino)
    xv, yv = extrai(rede, valid)
    cabeca = treina_cabeca(xt, yt)
    acerto = (cabeca(xv).argmax(dim=1) == yv).float().mean()
    p = parametros(rede) + parametros(cabeca)
    m = multiplicacoes(rede, foto)
    print(f"{nome:16} {p:11,} {p * 4 / 1e6:13.1f}"
          f" {m / 1e6:9.0f} M {acerto:7.1%}")
