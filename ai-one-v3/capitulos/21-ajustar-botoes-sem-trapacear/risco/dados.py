"""A tabela de treino, com as variáveis calculadas."""
import pandas as pd

from risco.alvo import carteira, com_alvo

TAXA = 0.045                          # juros ao mês
CORTE = pd.Timestamp("2025-07-01")  # a data que divide
LACRE = pd.Timestamp("2025-12-01")  # o teste: ninguém olha


def com_variaveis(t):
    """Acrescenta a parcela e o comprometimento declarado."""
    t = t.copy()
    n = t["parcelas"]
    t["parcela"] = t["valor"] * TAXA / (1 - (1 + TAXA) ** -n)
    fat = t["faturamento_declarado"]
    t["comprometimento"] = t["parcela"] / fat
    return t


def tabela():
    """Os empréstimos maduros, com alvo e variáveis."""
    return com_variaveis(com_alvo(carteira()))


def treino_validacao(t):
    """Divide no tempo: o passado treina, o recente valida."""
    antes = t["data_concessao"] < CORTE
    return t[antes], t[~antes]


def lacrar(t):
    """Separa os meses do teste, que só se abre uma vez."""
    antes = t["data_concessao"] < LACRE
    return t[antes], t[~antes]
