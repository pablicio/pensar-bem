import torch

from lauber.acervo import carrega, grade, partes
from lauber.classificador import Classificador, treina
from lauber.dcgan import (CODIGO, Gerador, Perito, inicia,
                          treina_dcgan)

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina(juiz, imgs[treino], familia[treino])


def variedade(x):
    """A distância média entre 200 estampas, duas a duas."""
    x = x[:200].flatten(1)
    return float(torch.cdist(x, x).mean())


torch.manual_seed(0)
gerador, perito = Gerador(), Perito()
gerador.apply(inicia)
perito.apply(inicia)
fixo = torch.randn(500, CODIGO)  # os mesmos 500 ruídos
fotos = treina_dcgan(gerador, perito, imgs[treino], 8,
                     fixo=fixo)
torch.save(gerador.state_dict(), "dcgan.pt")
print(f"variedade do acervo: {variedade(imgs[teste]):.1f}")
print("época  variedade  listra xadrez  poá floral cax geo")
for epoca, x in enumerate(fotos, start=1):
    vistas = torch.bincount(juiz(x).argmax(1), minlength=6)
    print(f"{epoca:5d} {variedade(x):10.1f} "
          + " ".join(f"{v:6d}" for v in vistas.tolist()))
grade(torch.cat([x[:8] for x in fotos]), "dcgan.png", 8)
