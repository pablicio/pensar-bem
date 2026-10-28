import warnings
from collections import Counter

import torch
from torch import nn

from dados.inverno import CARTOES, GABARITO, cartao_do_inverno
from leitora.carrega import leitora
from leitora.decide import REVISAO, limiar
from leitora.noite import le_cartao

torch.set_num_threads(1)
casa = leitora("modelos/leitora_casa.pt")
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    int8 = torch.ao.quantization.quantize_dynamic(
        casa, {nn.Linear}, dtype=torch.qint8)
LIMIAR = limiar(160, 3 * REVISAO)


def escrito(resposta, zeros):
    if resposta is None:
        return "   "
    return f"{resposta:03d}" if zeros else f"{resposta:>3d}"


def erros(alvo, texto):
    return sum(a != b for a, b in zip(alvo, texto))


c, erradas = Counter(), []
for i in range(CARTOES):
    inscricao, folha, respostas, zeros = cartao_do_inverno(i)
    leituras = zip(le_cartao(casa, folha),
                   le_cartao(int8, folha), respostas, GABARITO)
    for q, (a, b, certo, gab) in enumerate(leituras):
        (texto, lido, p), (texto8, lido8, _) = a, b
        alvo = escrito(certo, zeros)
        c["dígitos"] += sum(x != " " for x in alvo)
        c["float"] += erros(alvo, texto)
        c["int8"] += erros(alvo, texto8)
        c["discordam"] += lido != lido8
        if lido == "inválida" or p < LIMIAR:
            c["revisão"] += 1
        elif lido != certo:
            nota = (lido == gab) != (certo == gab)
            erradas.append((inscricao, q + 1, certo, lido, p,
                            nota))

n = 10 * CARTOES
print(f"cartões: {CARTOES:,}, respostas: {n:,},"
      f" dígitos escritos: {c['dígitos']:,}")
for nome in ["float", "int8"]:
    print(f"acerto por dígito, {nome}:"
          f" {1 - c[nome] / c['dígitos']:.3%}")
print(f"respostas em que os dois discordam: {c['discordam']}")
rev = c["revisão"]
print(f"revisão: {rev:,} respostas ({rev / n:.1%}),"
      f" R$ {rev * 3 * REVISAO:,.0f}")
print(f"lidas sozinhas: {n - rev:,},"
      f" erradas: {len(erradas)}")
for inscricao, q, certo, lido, p, nota in erradas:
    muda = ", muda a nota" if nota else ""
    print(f"  {inscricao} questão {q:2}: escreveu {certo},"
          f" leu {lido}, {p:.4f}{muda}")
