import torch

from lauber.acervo import FAMILIAS, carrega, grade, partes
from lauber.classificador import Classificador, treina
from lauber.dcgan import CODIGO, inicia
from lauber.encomenda import (GeradorPorFamilia,
                              PeritoPorFamilia,
                              desenha_familia,
                              treina_por_familia)

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina(juiz, imgs[treino], familia[treino])


def variedade(x):
    x = x[:200].flatten(1)
    return float(torch.cdist(x, x).mean())


torch.manual_seed(0)
gerador, perito = GeradorPorFamilia(), PeritoPorFamilia()
gerador.apply(inicia)
perito.apply(inicia)
treina_por_familia(gerador, perito, imgs[treino],
                   familia[treino], 8)
torch.save(gerador.state_dict(), "encomenda.pt")

torch.manual_seed(1)
z = torch.randn(500, CODIGO)        # os mesmos 500 ruídos
linhas = []
print("pedida      reconhecida  variedade  (acervo)")
for k, nome in enumerate(FAMILIAS):
    pedida = torch.full((500,), k)
    x = desenha_familia(gerador, z, pedida)
    certas = (juiz(x).argmax(1) == k).float().mean()
    reais = imgs[teste][familia[teste] == k]
    print(f"{nome:11} {certas:11.0%} {variedade(x):10.1f}"
          f" {variedade(reais):9.1f}")
    linhas.append(x[:8])
grade(torch.cat(linhas), "encomenda.png", colunas=8)

# a encomenda: doze florais e oito listras
pedido = torch.tensor([3] * 12 + [0] * 8)
x = desenha_familia(gerador, torch.randn(20, CODIGO), pedido)
vistas = juiz(x).argmax(1)
for k in (3, 0):
    print(f"{FAMILIAS[k]}: {int((pedido == k).sum())} pedidas,"
          f" {int(((pedido == k) & (vistas == k)).sum())}"
          f" reconhecidas")
grade(x, "pedido.png", colunas=10)
