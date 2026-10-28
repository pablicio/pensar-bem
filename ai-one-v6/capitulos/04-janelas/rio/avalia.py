"""Medidas de erro de uma previsão de nível."""
import numpy as np
import pandas as pd

PARTES = {"treino": ("1983", "2002"),
          "validacao": ("2003", "2007"),
          "teste": ("2008", "2026")}


def parte(serie, nome):
    """O trecho da série de uma das três partes, pelos anos."""
    inicio, fim = PARTES[nome]
    return serie.loc[inicio:fim]


def mae(erro):
    return float(np.nanmean(np.abs(erro)))


def rmse(erro):
    return float(np.sqrt(np.nanmean(np.square(erro))))


def picos(serie, cota=5.5):
    """A hora do pico de cada trecho da série acima da cota."""
    acima = serie.interpolate(limit=3) >= cota
    trecho = (acima != acima.shift()).cumsum()[acima]
    return list(serie[acima].groupby(trecho).idxmax())


def erro_nos_picos(serie, variacao, horas, h):
    """O erro da previsão feita h horas antes de cada pico."""
    prevista = serie.loc[horas].to_numpy() + variacao
    prevista = dict(zip(horas, prevista))
    return [prevista[p - pd.Timedelta(h, "h")] - serie[p]
            for p in picos(parte(serie, "teste"))]
