"""A regra de reserva, para quando a entrada sai do treino."""
import numpy as np

from rio.avalia import parte
from rio.entradas import CHUVAS


def chuva_24h(tab):
    colunas = [f"chuva_{c}" for c in CHUVAS]
    return tab[colunas].rolling(24).sum()


def fora_da_faixa(tab):
    """As horas em que o nível da cidade ou a chuva de 24 horas
    de algum posto passa do maior valor do treino."""
    chuva = chuva_24h(tab)
    teto_chuva = parte(chuva, "treino").max()
    teto_nivel = parte(tab, "treino")["cidade"].max()
    return ((tab["cidade"] > teto_nivel)
            | (chuva > teto_chuva).any(axis=1))


def com_reserva(previsto, nivel, horas, fora):
    """Nas horas fora da faixa, a previsão de cada horizonte é
    a maior entre a da rede e a da tendência de 6 horas."""
    subida = ((nivel - nivel.shift(6)) / 6).loc[horas]
    h = np.arange(1, previsto.shape[1] + 1)
    tendencia = subida.to_numpy()[:, None] * h
    fora = fora.loc[horas].to_numpy()[:, None]
    return np.where(fora, np.maximum(previsto, tendencia),
                    previsto)
