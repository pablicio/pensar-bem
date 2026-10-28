"""Camadas que sabem ir e voltar, um lote de cada vez."""
import numpy as np


class Linear:
    """Y = X W + b, com X de formato (lote, entradas)."""

    def __init__(self, entradas, saidas, sorteio):
        escala = np.sqrt(2 / entradas)      # o capítulo 14
        self.W = sorteio.normal(0, escala, (entradas, saidas))
        self.b = np.zeros(saidas)

    def frente(self, X):
        self.X = X                  # a volta vai precisar
        return X @ self.W + self.b

    def volta(self, dY):
        self.dW = self.X.T @ dY     # soma sobre o lote
        self.db = dY.sum(axis=0)
        return dY @ self.W.T        # para a camada anterior

    def parametros(self):
        return [(self.W, "dW"), (self.b, "db")]


class ReLU:
    def frente(self, X):
        self.ligado = X > 0
        return X * self.ligado

    def volta(self, dY):
        return dY * self.ligado     # passa só onde ligou

    def parametros(self):
        return []


def softmax_entropia(Z, y):
    """A perda média do lote e o gradiente em relação a Z."""
    Z = Z - Z.max(axis=1, keepdims=True)    # o capítulo 6
    log_p = Z - np.log(np.exp(Z).sum(axis=1, keepdims=True))
    n = len(y)
    perda = -log_p[np.arange(n), y].mean()
    dZ = np.exp(log_p)
    dZ[np.arange(n), y] -= 1        # softmax − rótulo
    return perda, dZ / n


class Rede:
    def __init__(self, tamanhos, semente=0):
        sorteio = np.random.default_rng(semente)
        self.camadas = []
        for a, b in zip(tamanhos, tamanhos[1:]):
            self.camadas += [Linear(a, b, sorteio), ReLU()]
        self.camadas.pop()          # sem ReLU no fim

    def frente(self, X):
        for c in self.camadas:
            X = c.frente(X)
        return X

    def volta(self, dZ):
        for c in reversed(self.camadas):
            dZ = c.volta(dZ)

    def parametros(self):
        return [(c, p, g) for c in self.camadas
                for p, g in c.parametros()]
