def soma(u, v):
    resultado = []
    for a, b in zip(u, v):
        resultado.append(a + b)
    return resultado


def escalar(k, v):
    resultado = []
    for a in v:
        resultado.append(k * a)
    return resultado


def media(vetores):
    total = vetores[0]
    for v in vetores[1:]:
        total = soma(total, v)
    return escalar(1 / len(vetores), total)
