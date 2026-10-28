"""Horários das fontes no fuso de Brasília."""
import pandas as pd

FUSO = "America/Sao_Paulo"


def cocalzinho_local(inicio):
    """O instante de cada leitura do fabricante B, em Brasília.

    Até 11/2/2027 a API mandava o horário de Brasília, sem
    fuso; desde 12/2/2027 (API v2), manda UTC, com 'Z' no fim.
    """
    utc = inicio.str.endswith("Z")
    em_utc = pd.to_datetime(inicio[utc], utc=True)
    de_utc = em_utc.dt.tz_convert(FUSO)
    locais = pd.to_datetime(inicio[~utc]).dt.tz_localize(FUSO)
    return pd.concat([de_utc, locais]).sort_index()
