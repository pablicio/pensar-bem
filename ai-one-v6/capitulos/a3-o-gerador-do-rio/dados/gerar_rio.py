"""Grava a telemetria das estações e os cadernos da régua."""
from pathlib import Path

import numpy as np
import pandas as pd

from dados.bacia import rio
from dados.chuva import gerar

PASTA = Path("dados/brutos")
CORTE = pd.Timestamp("2027-03-01")       # o livro começa aqui
REGUA_NOVA = pd.Timestamp("1996-07-01")  # a régua mudou
DEGRAU_CM = 37                 # o zero novo ficou 37 cm abaixo


def falhas(sorteio, n, quantas, maximo):
    """Uma máscara com `quantas` falhas de até `maximo` h."""
    falta = np.zeros(n, dtype=bool)
    for _ in range(quantas):
        i = int(sorteio.integers(0, n))
        falta[i:i + int(sorteio.integers(2, maximo))] = True
    return falta


def telemetria(chuva, niveis, sorteio):
    """As estações automáticas: nível em cm, chuva em mm."""
    tab = chuva.copy()
    for nome in ("rio_do_sul", "apiuna"):
        ruido = sorteio.normal(0, 0.8, len(tab))
        tab[f"nivel_{nome}"] = np.round(niveis[nome] * 100
                                        + ruido)
    n = len(tab)
    for col in tab.columns:
        tab.loc[falhas(sorteio, n, 40, 120), col] = np.nan
    # Apiúna fica sem energia quando chove forte em cima dela
    forte = chuva["apiuna"].rolling(3).sum().to_numpy() > 25
    apagao = forte & (sorteio.random(n) < 0.6)
    for i in np.flatnonzero(apagao):
        tab.iloc[i:i + 8, [3, 5]] = np.nan
    # e, em 2019, o sensor de nível de Apiúna travou seis dias
    travou = slice("2019-03-11 04:00", "2019-03-17 09:00")
    preso = tab.loc["2019-03-11 03:00", "nivel_apiuna"]
    tab.loc[travou, "nivel_apiuna"] = preso
    tab.index.name = "data_hora"
    return tab


def cadernos(nivel_cidade, horas, sorteio):
    """As leituras do Seu Nivaldo na régua da ponte, em cm."""
    leitura = pd.Series(nivel_cidade * 100, index=horas)
    leitura = leitura + sorteio.normal(0, 1.2, len(leitura))
    leitura[leitura.index >= REGUA_NOVA] += DEGRAU_CM
    antes = leitura.index < REGUA_NOVA
    leitura = leitura[~antes | (leitura.index.hour % 3 == 0)]
    fica = sorteio.random(len(leitura)) > 0.006
    fica &= ~((leitura.index >= "1990-06-04")
              & (leitura.index < "1990-06-27"))
    leitura = leitura[fica].round().astype(int)
    for i in sorteio.integers(0, len(leitura), 5):
        leitura.iloc[i] *= 10    # um zero a mais, digitando
    return leitura


def main():
    chuva = gerar()
    niveis = rio(chuva)
    sorteio = np.random.default_rng(61)
    PASTA.mkdir(parents=True, exist_ok=True)
    tele = telemetria(chuva, niveis, sorteio)
    tele[tele.index < CORTE].to_csv(PASTA / "telemetria.csv")
    regua = cadernos(niveis["cidade"], chuva.index, sorteio)
    tab = pd.DataFrame({"leitura_cm": regua})
    tab.index.name = "data_hora"
    tab[tab.index < CORTE].to_csv(PASTA / "cadernos.csv")
    # 2027: o que o sistema de alerta vai receber, hora a hora
    ruido = sorteio.normal(0, 0.8, len(tele))
    tele["nivel_cidade"] = np.round(niveis["cidade"] * 100
                                    + DEGRAU_CM + ruido)
    depois = tele[tele.index >= CORTE]
    depois.to_csv(PASTA / "temporada_2027.csv")
    for nome in ("telemetria", "cadernos", "temporada_2027"):
        tam = (PASTA / f"{nome}.csv").stat().st_size
        print(f"{nome + '.csv':20} {tam:>12,} bytes")


if __name__ == "__main__":
    main()
