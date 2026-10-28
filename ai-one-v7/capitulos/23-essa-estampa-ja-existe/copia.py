import numpy as np
import torch

from lauber.acervo import carrega, grade, partes
from lauber.dcgan import CODIGO, Gerador, desenha
from lauber.vizinhos import vizinho

imgs, _ = carrega()
treino, _, teste = partes(len(imgs))
gerador = Gerador()
gerador.load_state_dict(torch.load("dcgan.pt"))
torch.manual_seed(1)
geradas = desenha(gerador, torch.randn(500, CODIGO))

print("correlação com a mais parecida do treino")
print("               mediana    99%   máxima")
for nome, x in (("geradas", geradas),
                ("teste", imgs[teste][:500])):
    _, s = vizinho(x, imgs[treino], espelho=True)
    q = np.quantile(s, [0.5, 0.99, 1.0])
    print(f"{nome:13} {q[0]:8.3f} {q[1]:7.3f} {q[2]:7.3f}")

qual, s = vizinho(geradas[:6], imgs[treino], espelho=True)
grade(torch.cat([geradas[:6], imgs[treino][qual]]),
      "copia.png", colunas=6)
