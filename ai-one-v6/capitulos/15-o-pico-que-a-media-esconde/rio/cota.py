"""A previsão julgada pela cota: cheias avisadas, perdidas e
alarmes falsos."""
import pandas as pd

from rio.avalia import parte

HORA = pd.Timedelta("1h")


def grupos(horas, folga="24h"):
    """Junta horas próximas em eventos [início, fim]."""
    eventos, folga = [], pd.Timedelta(folga)
    for h in horas:
        if eventos and h - eventos[-1][1] <= folga:
            eventos[-1][1] = h
        else:
            eventos.append([h, h])
    return eventos


def julga(nivel, previsto, horas, cota=5.5, frente=12):
    """`previsto`: o nível máximo previsto para as próximas
    `frente` horas, em cada hora de `horas`. Alarme quando ele
    passa da cota; cheia quando o rio passa de verdade."""
    teste = parte(nivel, "teste")
    acima = teste.interpolate(limit=3) >= cota
    comeca = acima & ~acima.shift(1, fill_value=False)
    cheias = grupos(teste.index[comeca], "72h")
    alarme = pd.Series(previsto >= cota, index=horas)
    alarmes = grupos(alarme.index[alarme])
    antecedencia = []
    for inicio, _ in cheias:
        antes = alarme.loc[inicio - frente * HORA:
                           inicio - HORA]
        if antes.any():
            primeiro = antes.index[antes][0]
            antecedencia.append((inicio - primeiro) / HORA)
    falsos = 0
    for inicio, fim in alarmes:
        depois = teste.loc[inicio:fim + frente * HORA]
        falsos += bool(depois.max() < cota)
    return len(cheias), antecedencia, len(alarmes), falsos
