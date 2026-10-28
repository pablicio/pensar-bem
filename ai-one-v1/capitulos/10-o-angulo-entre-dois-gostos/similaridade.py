from distancias import norma


def produto_escalar(u, v):
    total = 0
    for a, b in zip(u, v):
        total += a * b
    return total


def cosseno(u, v):
    return produto_escalar(u, v) / (norma(u) * norma(v))
