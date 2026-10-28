"""Explicar uma decisão: e se uma coluna fosse a típica?"""
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype


def tipico(t, coluna):
    """A mediana de um número; o valor mais comum do resto."""
    x = t[coluna]
    if is_numeric_dtype(x) and not is_bool_dtype(x):
        return x.median()
    return x.mode()[0]


def e_se(modelo, pedido, base, colunas):
    """Quanto o risco muda trocando cada coluna pela típica."""
    risco = modelo.predict_proba(pedido[colunas])[0, 1]
    linhas = []
    for c in colunas:
        outro = pedido.copy()
        outro[c] = tipico(base, c)
        novo = modelo.predict_proba(outro[colunas])[0, 1]
        linhas.append({"coluna": c, "dela": pedido[c].iloc[0],
                       "típico": outro[c].iloc[0],
                       "muda": novo - risco})
    tabela = pd.DataFrame(linhas).set_index("coluna")
    return risco, tabela.sort_values("muda")
