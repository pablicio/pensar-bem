"""Os atrasados com todas as colunas: 23 números cada."""
import pandas as pd

from atrasos import PERFIL, atrasados


def tabela_larga():
    t = atrasados()
    negocio = pd.get_dummies(t["tipo_negocio"], dtype=float)
    extras = pd.DataFrame({
        "mei_mais": (t["produto"] == "MEI Mais").astype(float),
        "online": (t["canal"] == "online").astype(float)})
    X = pd.concat([t[PERFIL], negocio, extras], axis=1)
    return t, X
