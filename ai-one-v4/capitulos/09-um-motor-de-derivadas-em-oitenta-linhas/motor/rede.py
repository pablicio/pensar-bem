"""Neurônios, camadas e uma rede, feitos de Valor."""
import random

from motor.valor import Valor


class Neuronio:
    def __init__(self, entradas, ativacao=True):
        self.w = [Valor(random.uniform(-1, 1))
                  for _ in range(entradas)]
        self.b = Valor(0.0)
        self.ativacao = ativacao

    def __call__(self, x):
        termos = (wi * xi for wi, xi in zip(self.w, x))
        soma = sum(termos, self.b)
        return soma.tanh() if self.ativacao else soma

    def parametros(self):
        return self.w + [self.b]


class Camada:
    def __init__(self, entradas, saidas, ativacao=True):
        self.neuronios = [Neuronio(entradas, ativacao)
                          for _ in range(saidas)]

    def __call__(self, x):
        return [n(x) for n in self.neuronios]

    def parametros(self):
        return [p for n in self.neuronios
                for p in n.parametros()]


class Rede:
    """Camadas em sequência; a última sem ativação."""

    def __init__(self, tamanhos):
        pares = list(zip(tamanhos, tamanhos[1:]))
        ultima = len(pares) - 1
        self.camadas = [Camada(a, b, ativacao=i < ultima)
                        for i, (a, b) in enumerate(pares)]

    def __call__(self, x):
        for c in self.camadas:
            x = c(x)
        return x[0] if len(x) == 1 else x

    def parametros(self):
        return [p for c in self.camadas
                for p in c.parametros()]
