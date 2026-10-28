import numpy as np

from leitora.carrega import leitora
from leitora.decide import REVISAO, TEMPERATURA, limiar
from leitora.resposta import le_resposta

GABARITO = [42, 7, 315, 128, 9, 640, 77, 501, 18, 999]
IMPRESSOS = 1_450     # caracteres impressos num cartão
LIMIAR = limiar(160, 3 * REVISAO)   # três caixas por resposta

# o arquivo inteiro na memória, de uma vez
d = dict(np.load("dados/brutos/cartoes_verao.npz"))
cartoes = np.where(d["partes"] == "validacao")[0]


def escrito(resposta, zeros):
    """O que as três caixas deveriam conter."""
    if resposta < 0:
        return "   "
    return f"{resposta:03d}" if zeros else f"{resposta:>3d}"


def confere(modelo, t):
    """Conta os erros de cada tamanho nos cartões."""
    chaves = ["dígitos", "erros", "respostas", "notas",
              "candidatos", "revisão", "escapam"]
    c = dict.fromkeys(chaves, 0)
    for n in cartoes:
        folha, notas = d["folhas"][n], 0
        for q in range(10):
            r = int(d["respostas"][n][q])
            verdade = None if r < 0 else r
            certo = escrito(r, d["zeros"][n])
            texto, lido, p = le_resposta(modelo, folha, q, t)
            c["dígitos"] += sum(a != " " for a in certo)
            pares = zip(certo, texto)
            c["erros"] += sum(a != b for a, b in pares)
            c["respostas"] += lido != verdade
            gab = GABARITO[q]
            notas += (lido == gab) != (verdade == gab)
            if lido == "inválida" or p < LIMIAR:
                c["revisão"] += 1
            else:
                c["escapam"] += lido != verdade
        c["notas"] += notas
        c["candidatos"] += notas > 0
    return c


caracteres = (IMPRESSOS + 30) * len(cartoes)


def taxas(c):
    t = caracteres
    return {"acerto por caractere": 1 - c["erros"] / t,
            "acerto por dígito": 1 - c["erros"] / c["dígitos"],
            "acerto por resposta": 1 - c["respostas"] / 600}


mnist = confere(leitora("modelos/leitora_mnist.pt"), 1.315)
casa = confere(leitora("modelos/leitora_casa.pt"), TEMPERATURA)
tm, tc = taxas(mnist), taxas(casa)
print(f"limiar por resposta: {LIMIAR:.3f}\n")
print(f"{'':24} {'mnist':>7} {'casa':>7}")
for nome in tm:
    print(f"{nome:24} {tm[nome]:7.2%} {tc[nome]:7.2%}")
for nome, chave in [("questões, nota errada", "notas"),
                    ("candidatos, nota errada", "candidatos"),
                    ("respostas na revisão", "revisão"),
                    ("erradas entre as lidas", "escapam")]:
    print(f"{nome:24} {mnist[chave]:7} {casa[chave]:7}")
