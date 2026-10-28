import torch

from lauber.acervo import carrega, grade, partes
from lauber.classificador import Classificador, treina
from lauber.dcgan import CODIGO, Perito, desenha, inicia
from lauber.emenda import (GeradorCircular, costura, ladrilho,
                           treina_emenda)
from lauber.medidas import (caracteristicas, frechet,
                            precisao_cobertura)

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina(juiz, imgs[treino], familia[treino])

torch.manual_seed(0)
gerador, perito = GeradorCircular(), Perito()
gerador.apply(inicia)
perito.apply(inicia)
treina_emenda(gerador, perito, imgs[treino], 8)
torch.save(gerador.state_dict(), "emenda.pt")

torch.manual_seed(1)
geradas = desenha(gerador, torch.randn(1000, CODIGO))
print(f"costura: {costura(geradas):.2f}")
reais = caracteristicas(juiz, imgs[teste][:1000])
f = caracteristicas(juiz, geradas)
p, c = precisao_cobertura(reais, f)
print(f"Fréchet {frechet(reais, f):.1f}, precisão {p:.0%},"
      f" cobertura {c:.0%}")
grade(torch.stack([ladrilho(x) for x in geradas[:2]]),
      "ladrilho_emenda.png", colunas=2)
