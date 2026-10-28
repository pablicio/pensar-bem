"""Uma série vira exemplos de treino: janelas do passado."""
import numpy as np


def janelas(serie, passado, h, passo=1):
    """Para cada hora t: as `passado` horas até t, relativas
    a y_t, e o alvo y_(t+h) - y_t. Janelas com falta saem."""
    y = serie.to_numpy()
    deslizante = np.lib.stride_tricks.sliding_window_view
    vistas = deslizante(y, passado)
    t = np.arange(passado - 1, len(y) - h)[::passo]
    x = vistas[t - passado + 1] - y[t, None]
    alvo = y[t + h] - y[t]
    ok = ~np.isnan(x).any(axis=1) & ~np.isnan(alvo)
    return x[ok], alvo[ok], serie.index[t[ok]]
