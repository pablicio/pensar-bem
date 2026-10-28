import math


def binomial(k, n, p):
    # chance de k sucessos em n tentativas de chance p
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def poisson(k, lam):
    # chance de k eventos quando a média é lam
    return lam ** k * math.exp(-lam) / math.factorial(k)


def normal(x, media, desvio):
    # a altura da curva normal no ponto x
    z = (x - media) / desvio
    return (math.exp(-z ** 2 / 2)
            / (desvio * math.sqrt(2 * math.pi)))
