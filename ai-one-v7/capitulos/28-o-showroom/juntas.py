import torch

from lauber.acervo import carrega, partes
from lauber.dcgan import CODIGO, inicia
from lauber.encomenda import (PeritoPorFamilia,
                              desenha_familia,
                              treina_por_familia)
from lauber.vitrine import GeradorDaColecao, parecenca

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
gerador, perito = GeradorDaColecao(), PeritoPorFamilia()
gerador.apply(inicia)
perito.apply(inicia)
treina_por_familia(gerador, perito, imgs[treino],
                   familia[treino], 8)
torch.manual_seed(2)
print("família   parecença: geradas  acervo")
for k, nome in ((3, "floral"), (0, "listra")):
    x = desenha_familia(gerador, torch.randn(200, CODIGO),
                        torch.full((200,), k))
    reais = imgs[teste][familia[teste] == k][:200]
    print(f"{nome:9} {parecenca(x):18.2f}"
          f" {parecenca(reais):7.2f}")
