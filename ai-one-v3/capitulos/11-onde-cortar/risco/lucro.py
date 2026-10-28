"""O dinheiro de cada decisão de crédito."""
import numpy as np

MARGEM = 0.40    # fração dos juros que vira lucro


def ganho(t, margem=MARGEM):
    """Quanto cada empréstimo deu (ou tirou), se aprovado."""
    juros = t["parcela"] * t["parcelas"] - t["valor"]
    bom = margem * juros
    perda = -t["saldo_devedor"]
    return np.where(t["alvo"] == 0, bom, perda)


def lucro(p, valores, corte):
    """O lucro de aprovar quem fica abaixo do corte."""
    return valores[p < corte].sum()
