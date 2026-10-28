import pandas as pd


def rotuladas():
    """As 1.500 finalidades classificadas pelos agentes."""
    r = pd.read_csv("dados/brutos/finalidades_rotuladas.csv")
    e = pd.read_csv("dados/brutos/emprestimos.csv")
    return r.merge(e[["pedido_id", "finalidade"]],
                   on="pedido_id", validate="one_to_one")
