"""Camadas que sabem ir e voltar, um lote de cada vez."""
import numpy as np


class Linear:
    """Y = X W + b, com X de formato (lote, entradas)."""

    def __init__(self, entradas, saidas, sorteio, inicio="he"):
        escala = {"he": np.sqrt(2 / entradas),
                  "xavier": np.sqrt(1 / entradas),
                  "pequena": 0.01, "um": 1.0}[inicio]
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


class NormLote:
    """Normaliza cada neurônio pela média e desvio do lote."""

    def __init__(self, n, momento=0.9, eps=1e-5):
        self.gama, self.beta = np.ones(n), np.zeros(n)
        self.media_run, self.var_run = np.zeros(n), np.ones(n)
        self.momento, self.eps = momento, eps
        self.treinando = True

    def frente(self, X):
        if self.treinando:                  # as contas do lote
            media, var = X.mean(axis=0), X.var(axis=0)
            m = self.momento
            self.media_run = (m * self.media_run
                              + (1 - m) * media)
            self.var_run = m * self.var_run + (1 - m) * var
        else:                               # as guardadas
            media, var = self.media_run, self.var_run
        self.desvio = np.sqrt(var + self.eps)
        self.Xn = (X - media) / self.desvio
        return self.gama * self.Xn + self.beta

    def volta(self, dY):
        self.dgama = (dY * self.Xn).sum(axis=0)
        self.dbeta = dY.sum(axis=0)
        dXn = dY * self.gama
        # a média e o desvio também dependem de cada exemplo
        centro = dXn - dXn.mean(axis=0)
        giro = self.Xn * (dXn * self.Xn).mean(axis=0)
        return (centro - giro) / self.desvio

    def parametros(self):
        return [(self.gama, "dgama"), (self.beta, "dbeta")]


class Dropout:
    """No treino, desliga cada neurônio com probabilidade p."""

    def __init__(self, p, semente=0):
        self.p, self.treinando = p, True
        self.sorteio = np.random.default_rng(semente)

    def frente(self, X):
        if not self.treinando:
            return X                    # na avaliação, nada
        manter = self.sorteio.random(X.shape) >= self.p
        self.mascara = manter / (1 - self.p)   # compensa
        return X * self.mascara

    def volta(self, dY):
        return dY * self.mascara

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
    def __init__(self, tamanhos, semente=0, inicio="he",
                 normaliza=False, dropout=0.0):
        sorteio = np.random.default_rng(semente)
        self.camadas = []
        for a, b in zip(tamanhos, tamanhos[1:]):
            self.camadas.append(Linear(a, b, sorteio, inicio))
            if normaliza:
                self.camadas.append(NormLote(b))
            self.camadas.append(ReLU())
            if dropout:
                k = semente + len(self.camadas)  # uma cada
                self.camadas.append(Dropout(dropout, k))
        while not isinstance(self.camadas[-1], Linear):
            self.camadas.pop()      # nada depois da última

    def modo(self, treinando):
        """Treino: contas do lote; avaliação: as guardadas."""
        for c in self.camadas:
            if hasattr(c, "treinando"):
                c.treinando = treinando

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
