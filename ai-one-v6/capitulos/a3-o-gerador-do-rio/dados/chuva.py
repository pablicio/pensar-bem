"""A chuva de hora em hora nos quatro pluviômetros."""
import numpy as np
import pandas as pd

POSTOS = ["taio", "ituporanga", "rio_do_sul", "apiuna"]
HORAS = pd.date_range("1983-01-01", "2027-10-31 23:00",
                      freq="h")

# chance de começar uma chuva em cada dia, mês a mês: mais na
# primavera e no verão, menos no inverno
CHANCE = [.36, .36, .32, .24, .20, .20,
          .20, .21, .28, .32, .32, .34]

# os eventos que a história precisa: (início, horas, chuva
# média total em mm, peso em cada posto)
MARCADOS = [
    ("1983-07-05 06:00", 110, 340, (1.1, 1.1, 1.0, 0.8)),
    ("1984-08-06 12:00", 70, 110, (1.0, 1.1, 1.0, 0.9)),
    ("1992-05-28 00:00", 60, 160, (0.9, 1.0, 1.1, 1.0)),
    ("2008-11-12 00:00", 240, 75, (1.0, 1.0, 1.0, 1.0)),
    ("2008-11-22 06:00", 44, 270, (0.6, 0.7, 1.2, 1.5)),
    ("2011-09-07 00:00", 90, 250, (1.1, 1.0, 1.0, 0.9)),
    ("2023-10-05 00:00", 96, 235, (1.0, 1.1, 1.0, 0.9)),
    ("2023-11-16 12:00", 60, 200, (1.0, 1.0, 1.0, 1.0)),
    ("2026-10-14 13:00", 3, 20, (0.0, 0.0, 0.5, 2.2)),
    ("2027-10-08 00:00", 96, 235, (1.1, 1.0, 1.0, 1.0)),
]


# as frentes chegam pelo oeste: a chuva começa nas cabeceiras
# e alcança os postos rio abaixo algumas horas depois
ATRASO = [0, 1, 4, 7]


def evento(sorteio, horas, total, pesos):
    """Uma chuva: rajadas sorteadas, somando `total`."""
    forma = sorteio.gamma(0.7, size=horas) + 0.05
    forma = forma / forma.sum()
    ruido = sorteio.lognormal(0.0, 0.25, size=(horas, 4))
    chuva = total * forma[:, None] * np.array(pesos) * ruido
    saida = np.zeros((horas + max(ATRASO), 4))
    for j, a in enumerate(ATRASO):
        saida[a:a + horas, j] = chuva[:, j]
    return saida


def gerar(semente=6):
    sorteio = np.random.default_rng(semente)
    chuva = np.zeros((len(HORAS), 4))
    fator_ano = {a: sorteio.lognormal(0.0, 0.18)
                 for a in range(1983, 2028)}
    for dia in pd.date_range(HORAS[0], HORAS[-1], freq="D"):
        if sorteio.random() > CHANCE[dia.month - 1]:
            continue
        horas = int(np.clip(sorteio.gamma(2.0, 9.0), 2, 90))
        total = sorteio.gamma(1.3, 9.0) * fator_ano[dia.year]
        total = min(total, 45)
        pesos = sorteio.lognormal(0.0, 0.35, size=4)
        i = HORAS.get_loc(dia) + int(sorteio.integers(0, 24))
        e = evento(sorteio, horas, total, pesos)
        j = min(i + len(e), len(HORAS))
        chuva[i:j] += e[:j - i]
    for inicio, horas, total, pesos in MARCADOS:
        i = HORAS.get_loc(pd.Timestamp(inicio))
        e = evento(sorteio, horas, total, pesos)
        chuva[i:i + len(e)] += e
    return pd.DataFrame(np.round(chuva, 1), index=HORAS,
                        columns=POSTOS)
