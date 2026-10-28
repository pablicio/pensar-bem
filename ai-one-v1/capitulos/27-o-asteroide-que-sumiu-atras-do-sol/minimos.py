def perda(pares, a, b):
    # o erro quadrático médio da reta y = a x + b
    return sum((a * x + b - y) ** 2
               for x, y in pares) / len(pares)


def gradiente(pares, a, b):
    # as derivadas parciais da perda em relação a a e a b
    n = len(pares)
    da = sum(2 * (a * x + b - y) * x for x, y in pares) / n
    db = sum(2 * (a * x + b - y) for x, y in pares) / n
    return da, db


def descida(pares, eta, passos):
    # parte de a = b = 0 e anda contra o gradiente
    a, b = 0.0, 0.0
    historico = []
    for _ in range(passos):
        da, db = gradiente(pares, a, b)
        a, b = a - eta * da, b - eta * db
        historico.append(perda(pares, a, b))
    return a, b, historico


def solucao_fechada(pares):
    # o ponto em que as duas derivadas parciais valem zero
    n = len(pares)
    mx = sum(x for x, _ in pares) / n
    my = sum(y for _, y in pares) / n
    a = (sum((x - mx) * (y - my) for x, y in pares)
         / sum((x - mx) ** 2 for x, _ in pares))
    return a, my - a * mx
