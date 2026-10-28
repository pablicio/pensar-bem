"""Da chuva à vazão e da vazão ao nível: uma bacia simples."""
import numpy as np
from scipy.signal import lfilter

# as três sub-bacias: área em km², capacidade do solo em mm,
# tempo de resposta em horas e os pluviômetros de cada uma
SUB = {
    "cabeceiras": (5100, 190, 10,
                   {"taio": .5, "ituporanga": .5}),
    "meio": (4200, 170, 7,
             {"rio_do_sul": .7, "ituporanga": .3}),
    "local": (1700, 150, 4, {"apiuna": .8, "rio_do_sul": .2}),
}


def reservatorio(entrada, k, inicio=0.0):
    """Um reservatório linear: devolve 1/k do que guarda.

    `inicio` é a vazão de saída na hora zero."""
    zi = [(1 - 1 / k) * inicio]
    saida, _ = lfilter([1 / k], [1, -(1 - 1 / k)], entrada,
                       zi=zi)
    return saida


def nash(entrada, k, n=3):
    """n reservatórios em fila: sobe e desce suave."""
    for _ in range(n):
        entrada = reservatorio(entrada, k)
    return entrada


def solo(chuva, capacidade, evapora):
    """Quanto da chuva escorre, pelo quanto o solo está cheio.

    Devolve o escoamento rápido e o que percola."""
    s = 0.5 * capacidade
    rapido = np.empty_like(chuva)
    lento = np.empty_like(chuva)
    for t, p in enumerate(chuva):
        cheio = min(s / capacidade, 1.0)
        r = p * cheio ** 2.0
        perc = 0.0012 * s
        s = max(s + p - r - perc - evapora[t] * cheio, 0.0)
        rapido[t], lento[t] = r, perc
    return rapido, lento


def vazao(chuva, horas):
    """A vazão (m³/s) de cada sub-bacia, com a chuva dela."""
    dia = horas.dayofyear.to_numpy()
    angulo = 2 * np.pi * (dia - 15) / 365
    evapora = 0.10 + 0.06 * np.cos(angulo)
    saida = {}
    for nome, (area, cap, k, postos) in SUB.items():
        p = sum(peso * chuva[posto].to_numpy()
                for posto, peso in postos.items())
        rapido, lento = solo(p, cap, evapora)
        lencol = reservatorio(lento, 900, lento.mean())
        mm = nash(rapido, k / 2) + lencol
        saida[nome] = mm * area / 3.6     # mm/h × km² → m³/s
    return saida


def propaga(q, atraso, k):
    """A água que desce o rio: chega `atraso` horas depois."""
    atrasada = np.concatenate([np.full(atraso, q[0]),
                               q[:-atraso]])
    return reservatorio(atrasada, k, atrasada[0])


def nivel(q, zero, a, b):
    """A curva-chave: o nível na régua (m) para a vazão."""
    return zero + a * np.maximum(q, 0) ** b


def rio(chuva):
    """Os níveis de Rio do Sul, Apiúna e da cidade."""
    q = vazao(chuva, chuva.index)
    q_rds = q["cabeceiras"] + 25
    q_api = propaga(q_rds, 12, 3) + q["meio"] + 15
    q_cid = propaga(q_api, 6, 2) + q["local"] + 8
    return {"rio_do_sul": nivel(q_rds, 0.150, 0.0649, 0.60),
            "apiuna": nivel(q_api, 0.401, 0.0408, 0.60),
            "cidade": nivel(q_cid, 0.324, 0.0332, 0.60),
            "vazao_cidade": q_cid}
