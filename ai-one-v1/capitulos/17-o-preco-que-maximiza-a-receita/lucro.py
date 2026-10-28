from demanda import demanda

CUSTO = 38.00          # o que a fábrica cobra por cópia


def lucro(preco):
    return (preco - CUSTO) * demanda(preco)


def receita(preco):
    return preco * demanda(preco)
