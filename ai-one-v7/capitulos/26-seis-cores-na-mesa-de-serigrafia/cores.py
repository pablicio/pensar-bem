import numpy as np
import torch

from lauber.acervo import carrega, grade, partes
from lauber.dcgan import CODIGO, desenha
from lauber.emenda import GeradorCircular
from dados.estampas import PALETAS
from lauber.serigrafia import (delta_e, ilhas, limpa, reduz,
                               telas, tinta_mais_proxima)

imgs, _ = carrega()
_, _, teste = partes(len(imgs))
gerador = GeradorCircular()
gerador.load_state_dict(torch.load("emenda.pt"))
torch.manual_seed(1)
gerada = desenha(gerador, torch.randn(1, CODIGO))[0]
estampas = {"do acervo": imgs[teste][3],
            "gerada": gerada}
for nome, x in estampas.items():
    img = x.permute(1, 2, 0).numpy().astype(float)
    bytes8 = np.round(img * 255).reshape(-1, 3)
    distintas = len(np.unique(bytes8, axis=0))
    print(f"estampa {nome}: {distintas} cores distintas")
    erros = []
    for k in range(2, 9):
        rotulos, paleta = reduz(img, k)
        erros.append(delta_e(img, paleta[rotulos]))
    ks = " ".join(f"{k:5d}" for k in range(2, 9))
    print(f"  cores:   {ks}")
    es = " ".join(f"{e:5.1f}" for e in erros)
    print(f"  ΔE médio:{es}")

img = gerada.permute(1, 2, 0).numpy().astype(float)
rotulos, paleta = reduz(img, 6)
limpos = limpa(rotulos, 6)
for nome, r in (("reduzida", rotulos), ("limpa", limpos)):
    print(f"{nome:8}: {ilhas(r):3d} pontos soltos,"
          f" ΔE {delta_e(img, paleta[r]):.1f}")
tintas = np.array([c for cores in PALETAS.values()
                   for c in cores])
for k, cor in enumerate(paleta):
    t, d = tinta_mais_proxima(cor, tintas)
    print(f"cor {k}: tinta {t:2d} do estoque, ΔE {d:4.1f}")
print(f"seis telas: R$ {6 * 380:,}".replace(",", "."))

cores = torch.tensor(paleta, dtype=torch.float32)
reduzida = cores[torch.tensor(limpos)].permute(2, 0, 1)
separadas = [torch.where(torch.tensor(m), cor[:, None, None],
                         torch.ones(3, 1, 1))
             for m, cor in zip(telas(limpos, 6), cores)]
grade(torch.stack([gerada, reduzida, *separadas]),
      "telas.png", colunas=4)
