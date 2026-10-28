import time
import warnings

import torch
from torch import nn

from dados.inverno import CARTOES, cartao_do_inverno
from leitora.carrega import leitora
from leitora.noite import recorta

torch.set_num_threads(1)
casa = leitora("modelos/leitora_casa.pt")
with warnings.catch_warnings():
    warnings.simplefilter("ignore")     # obsoleta: ver o texto
    int8 = torch.ao.quantization.quantize_dynamic(
        casa, {nn.Linear}, dtype=torch.qint8)
total = {"cartões": CARTOES}


def cronometra(nome, funcao, n, unidade, vezes=1):
    """A melhor de algumas medidas, projetada para a noite."""
    melhor = float("inf")
    for _ in range(vezes):
        inicio = time.perf_counter()
        resultado = funcao()
        melhor = min(melhor, time.perf_counter() - inicio)
    noite = melhor / n * total[unidade]
    print(f"{nome:30} {n / melhor:9,.0f} {unidade}/s"
          f" {noite:6.0f} s")
    return resultado


def rede(modelo, lotes, modo):
    with modo():
        for x in lotes:
            modelo(x)


folhas = cronometra("gerar (o scanner)", lambda: [
    cartao_do_inverno(i)[1] for i in range(100)],
    100, "cartões")
cortes = cronometra("recortar", lambda: [
    recorta(f)[0] for f in folhas], 100, "cartões")
tudo = torch.cat(cortes)
n = len(tudo)
total["dígitos"] = CARTOES * n / 100

uma = [x[None] for x in tudo]
inf, cem = torch.inference_mode, [tudo]
com, sem = torch.enable_grad, torch.no_grad
for nome, modelo, lotes, modo in [
        ("uma caixa por vez", casa, uma, inf),
        ("um cartão por vez", casa, cortes, inf),
        ("cem cartões, com grafo", casa, cem, com),
        ("cem cartões, no_grad", casa, cem, sem),
        ("cem cartões, inference", casa, cem, inf),
        ("cem cartões, int8", int8, cem, inf)]:
    cronometra(nome, lambda: rede(modelo, lotes, modo),
               n, "dígitos", vezes=5)
