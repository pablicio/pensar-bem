"""A tabela do modelo com a região e o prefixo do telefone."""
import numpy as np
import pandas as pd

from risco.dados import lacrar, tabela, treino_validacao
from risco.finalidade import com_divida


def com_regiao():
    clientes = pd.read_csv("dados/brutos/clientes.csv")
    t = com_divida(tabela()).merge(
        clientes[["cliente_id", "regiao"]], on="cliente_id")
    fone = t["telefone_referencia"].str.replace(r"\D", "",
                                                regex=True)
    numero = fone.str[2:]
    # fixo: os quatro primeiros dígitos; celular: 0
    t["prefixo"] = np.where(numero.str.len() == 8,
                            numero.str[:4], "0").astype(int)
    return t


def divisao():
    """Treino e validação, sem tocar no teste lacrado."""
    aberto, _ = lacrar(com_regiao())
    return treino_validacao(aberto)
