import time

import torch
from torch.nn.functional import avg_pool2d

from lauber.acervo import carrega, grade, partes
from lauber.classificador import Classificador, treina
from lauber.dcgan import CODIGO, desenha, inicia, treina_dcgan
from lauber.medidas import caracteristicas, frechet
from lauber.resolucao import acervo_em, gerador, perito
from lauber.vitrine import parecenca

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina(juiz, imgs[treino], familia[treino])
reais = caracteristicas(juiz, imgs[teste][:1000])

print("lado  parâmetros  s/época  Fréchet  parecença")
linhas = []
for lado in (32, 64):
    dados = acervo_em(lado, 4000)
    torch.manual_seed(0)
    g, p = gerador(lado), perito(lado)
    g.apply(inicia)
    p.apply(inicia)
    inicio = time.perf_counter()
    treina_dcgan(g, p, dados, 6)
    por_epoca = (time.perf_counter() - inicio) / 6
    x = desenha(g, torch.randn(1000, CODIGO))
    vista = avg_pool2d(x, lado // 32)     # de volta a 32
    f = frechet(reais, caracteristicas(juiz, vista))
    n = sum(q.numel() for q in g.parameters())
    print(f"{lado:4d} {n:11,d} {por_epoca:8.1f} {f:8.1f}"
          f" {parecenca(vista[:300]):10.2f}")
    linhas.append(x[:6])
grade(linhas[0], "lado32.png", colunas=6)
grade(linhas[1], "lado64.png", colunas=6)
acervo = parecenca(imgs[teste][:300])
print(f"parecença do acervo: {acervo:.2f}")
