"""Cada derivada do livro contra a derivada numérica."""
import numpy as np

sorteio = np.random.default_rng(4)


def numerica(f, x, h=1e-6):
    """O gradiente de f, um número, por diferenças."""
    g = np.zeros_like(x)
    for i in np.ndindex(x.shape):
        guarda = x[i]
        x[i] = guarda + h
        mais = f(x)
        x[i] = guarda - h
        menos = f(x)
        x[i] = guarda
        g[i] = (mais - menos) / (2 * h)
    return g


def confere(nome, f, analitica, x):
    erro = np.abs(numerica(f, x) - analitica).max()
    print(f"{nome:30} {erro:9.1e}")


x = sorteio.normal(size=(4, 5))
G = sorteio.normal(size=(4, 5))     # dL/dsaída, sorteado
sig = lambda z: 1 / (1 + np.exp(-z))
confere("sigmoide", lambda z: (sig(z) * G).sum(),
        sig(x) * (1 - sig(x)) * G, x)
confere("tanh", lambda z: (np.tanh(z) * G).sum(),
        (1 - np.tanh(x) ** 2) * G, x)
confere("ReLU", lambda z: (np.maximum(0, z) * G).sum(),
        (x > 0) * G, x)

y = np.array([3, 0, 4, 1])           # as classes certas


def entropia(z):
    z = z - z.max(axis=1, keepdims=True)
    logp = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    return -logp[np.arange(len(y)), y].mean()


p = np.exp(x) / np.exp(x).sum(axis=1, keepdims=True)
confere("softmax + entropia cruzada", entropia,
        (p - np.eye(5)[y]) / len(y), x)

w, b, xs = 0.7, -0.2, 1.5
confere("erro quadrático, em w", lambda w: ((w * xs + b) ** 2),
        2 * (w * xs + b) * xs, np.array(w))

W = sorteio.normal(size=(5, 3))
bias = sorteio.normal(size=3)
Gy = sorteio.normal(size=(4, 3))
confere("camada linear, em W", lambda W: ((x @ W + bias) * Gy)
        .sum(), x.T @ Gy, W)
confere("camada linear, em b", lambda b: ((x @ W + b) * Gy)
        .sum(), Gy.sum(axis=0), bias)
confere("camada linear, em X", lambda X: ((X @ W + bias) * Gy)
        .sum(), Gy @ W.T, x)


def normaliza(z, eixo):
    media = z.mean(axis=eixo, keepdims=True)
    desvio = np.sqrt(z.var(axis=eixo, keepdims=True) + 1e-5)
    return (z - media) / desvio, desvio


for nome, eixo in [("normalização em lote", 0),
                   ("normalização de camada", 1)]:
    xh, desvio = normaliza(x, eixo)
    m = lambda a: a.mean(axis=eixo, keepdims=True)
    confere(nome, lambda z: (normaliza(z, eixo)[0] * G).sum(),
            (G - m(G) - xh * m(G * xh)) / desvio, x)

mascara = sorteio.random(x.shape) > 0.2
confere("dropout (p = 0,2)",
        lambda z: (z * mascara / 0.8 * G).sum(),
        mascara / 0.8 * G, x)
lam = 0.01
confere("L2, em W", lambda W: lam / 2 * (W ** 2).sum(),
        lam * W, W)
