import pandas as pd

NUMEROS = ["idade", "tempo_negocio_meses",
           "cliente_desde_meses", "emprestimos_anteriores",
           "atrasos_anteriores", "valor", "parcelas"]


def visitas():
    """As visitas dos agentes, com o pedido e a região."""
    v = pd.read_csv("dados/brutos/visitas.csv")
    e = pd.read_csv("dados/brutos/emprestimos.csv")
    c = pd.read_csv("dados/brutos/clientes.csv")
    t = v.merge(e, on="pedido_id", validate="one_to_one")
    regiao = c[["cliente_id", "regiao"]]
    return t.merge(regiao, on="cliente_id",
                   validate="many_to_one")
