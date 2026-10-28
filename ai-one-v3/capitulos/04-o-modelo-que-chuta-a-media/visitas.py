import pandas as pd

NUMEROS = ["idade", "tempo_negocio_meses",
           "cliente_desde_meses", "emprestimos_anteriores",
           "atrasos_anteriores", "valor", "parcelas"]


def visitas():
    """As visitas dos agentes, com os dados do pedido."""
    v = pd.read_csv("dados/brutos/visitas.csv")
    e = pd.read_csv("dados/brutos/emprestimos.csv")
    return v.merge(e, on="pedido_id", validate="one_to_one")
