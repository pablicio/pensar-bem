"""Medidas de erro de uma previsão de nível."""
import numpy as np

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
