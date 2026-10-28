"""Como dar o passo, depois de saber a direção."""
import numpy as np


class SGD:
    """Cada parâmetro anda contra o seu gradiente."""

    def __init__(self, rede, taxa, decaimento=0.0):
        self.rede, self.taxa = rede, taxa
        self.decaimento = decaimento

    def grad(self, camada, valor, nome):
        """O gradiente, mais o decaimento dos pesos (o L2)."""
        g = getattr(camada, nome)
        if nome == "dW" and self.decaimento:
            g = g + self.decaimento * valor
        return g

    def passo(self):
        for camada, valor, nome in self.rede.parametros():
            valor -= self.taxa * self.grad(camada, valor, nome)


class Momento(SGD):
    """O passo lembra a direção dos passos anteriores."""

    def __init__(self, rede, taxa, beta=0.9, decaimento=0.0):
        super().__init__(rede, taxa, decaimento)
        self.beta, self.v = beta, {}

    def passo(self):
        for camada, valor, nome in self.rede.parametros():
            g = self.grad(camada, valor, nome)
            v = self.v.get(id(valor), np.zeros_like(valor))
            v = self.beta * v + g
            self.v[id(valor)] = v
            valor -= self.taxa * v


class Adam(SGD):
    """Momento, e um passo medido pelo tamanho do gradiente."""

    def __init__(self, rede, taxa=1e-3, b1=0.9, b2=0.999,
                 eps=1e-8, decaimento=0.0):
        super().__init__(rede, taxa, decaimento)
        self.b1, self.b2, self.eps = b1, b2, eps
        self.m, self.s, self.t = {}, {}, 0

    def passo(self):
        self.t += 1
        for camada, valor, nome in self.rede.parametros():
            g = self.grad(camada, valor, nome)
            k = id(valor)
            m = self.b1 * self.m.get(k, 0) + (1 - self.b1) * g
            s = (self.b2 * self.s.get(k, 0)
                 + (1 - self.b2) * g * g)
            self.m[k], self.s[k] = m, s
            m_hat = m / (1 - self.b1 ** self.t)     # correção
            s_hat = s / (1 - self.b2 ** self.t)     # do começo
            passo = m_hat / (np.sqrt(s_hat) + self.eps)
            valor -= self.taxa * passo
