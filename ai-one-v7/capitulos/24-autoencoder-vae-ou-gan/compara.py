import time

import torch

from lauber.acervo import carrega, grade, partes
from lauber.autoencoder import Denso, treina
from lauber.classificador import Classificador
from lauber.classificador import treina as treina_juiz
from lauber.dcgan import (CODIGO, Gerador, Perito, desenha,
                          inicia, treina_dcgan)
from lauber.encomenda import (GeradorPorFamilia,
                              PeritoPorFamilia,
                              desenha_familia,
                              treina_por_familia)
from lauber.medidas import (caracteristicas, frechet,
                            precisao_cobertura)
from lauber.vae import VAE, treina_vae

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina_juiz(juiz, imgs[treino], familia[treino])
N = 1000
reais = caracteristicas(juiz, imgs[teste][:N])
x, f = imgs[treino], familia[treino]
resultados, linhas = {}, []


def mede(nome, segundos, amostras, controle="-"):
    linhas.append(amostras[:8])
    c = caracteristicas(juiz, amostras)
    p, cob = precisao_cobertura(reais, c)
    resultados[nome] = (frechet(reais, c), p, cob, segundos,
                        controle)


# o autoencoder do capítulo 3, sorteando códigos de uma
# gaussiana ajustada aos códigos do treino
torch.manual_seed(0)
inicio = time.perf_counter()
ae = Denso(codigo=16)
treina(ae, x, epocas=10)
with torch.no_grad():
    codigos = ae.codificador(x)
    gauss = torch.distributions.MultivariateNormal(
        codigos.mean(0), torch.cov(codigos.T))
    amostras = ae.decodificador(gauss.sample((N,)))
mede("autoencoder", time.perf_counter() - inicio, amostras)

torch.manual_seed(0)
inicio = time.perf_counter()
vae = VAE(codigo=16, convolucional=True)
treina_vae(vae, x, epocas=4)
vae.eval()
with torch.no_grad():
    amostras = vae.decodificador(torch.randn(N, 16))
mede("VAE", time.perf_counter() - inicio, amostras)

torch.manual_seed(0)
inicio = time.perf_counter()
g, p = Gerador(), Perito()
g.apply(inicia)
p.apply(inicia)
treina_dcgan(g, p, x, 8)
amostras = desenha(g, torch.randn(N, CODIGO))
mede("DCGAN", time.perf_counter() - inicio, amostras)

torch.manual_seed(0)
inicio = time.perf_counter()
g, p = GeradorPorFamilia(), PeritoPorFamilia()
g.apply(inicia)
p.apply(inicia)
treina_por_familia(g, p, x, f, 8)
segundos = time.perf_counter() - inicio
pedidas = f[torch.randint(len(f), (N,))]
amostras = desenha_familia(g, torch.randn(N, CODIGO), pedidas)
certas = (juiz(amostras).argmax(1) == pedidas).float().mean()
mede("GAN condicional", segundos, amostras, f"{certas:.0%}")

print("gerador          Fréchet precisão cobertura  treino"
      "  família")
for nome, (fr, p, c, s, ctl) in resultados.items():
    print(f"{nome:16} {fr:7.1f} {p:8.0%} {c:9.0%} {s:6.0f} s"
          f" {ctl:>8}")
grade(torch.cat(linhas), "compara.png", colunas=8)
