import math

from sigmoide import sigmoide


def f1(x):
    return 3 * x ** 2 + 2 * x


def d1(x):
    return 6 * x + 2  # potência, constante e soma


def f2(x):
    return x * math.exp(x)


def d2(x):
    return math.exp(x) + x * math.exp(x)  # regra do produto


def f3(x):
    return math.log(x)


def d3(x):
    return 1 / x


def f4(x):
    return sigmoide(3 - 0.04 * x)


def d4(x):
    s = sigmoide(3 - 0.04 * x)
    return s * (1 - s) * (-0.04)  # regra da cadeia


h = 1e-5
pontos = [0.5 * k for k in range(1, 11)]
for nome, f, d in [("3x² + 2x", f1, d1), ("x e^x", f2, d2),
                   ("ln x", f3, d3), ("σ(3 − 0,04x)", f4, d4)]:
    pior = 0
    for x in pontos:
        numerica = (f(x + h) - f(x - h)) / (2 * h)
        pior = max(pior, abs(numerica - d(x)))
    print(f"{nome:14s} maior diferença: {pior:.1e}")
