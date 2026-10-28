"""Um motor de derivadas automáticas, um número de cada vez."""
import math


class Valor:
    """Um número que lembra de onde veio e sabe derivar."""

    def __init__(self, dado, filhos=()):
        self.dado = float(dado)
        self.grad = 0.0                # dL/d(este valor)
        self._filhos = filhos          # quem o produziu
        self._volta = lambda: None     # leva o grad aos filhos

    def __repr__(self):
        return f"Valor({self.dado:.4f}, grad={self.grad:.4f})"

    @staticmethod
    def _v(x):
        return x if isinstance(x, Valor) else Valor(x)

    def __add__(self, outro):
        outro = Valor._v(outro)
        saida = Valor(self.dado + outro.dado, (self, outro))

        def volta():                   # a soma passa igual
            self.grad += saida.grad
            outro.grad += saida.grad
        saida._volta = volta
        return saida

    def __mul__(self, outro):
        outro = Valor._v(outro)
        saida = Valor(self.dado * outro.dado, (self, outro))

        def volta():                   # cada lado leva o outro
            self.grad += outro.dado * saida.grad
            outro.grad += self.dado * saida.grad
        saida._volta = volta
        return saida

    def _unaria(self, f, df):          # f e a derivada dela
        saida = Valor(f(self.dado), (self,))

        def volta():
            self.grad += df(self.dado, saida.dado) * saida.grad
        saida._volta = volta
        return saida

    def __pow__(self, k):              # k é um número comum
        return self._unaria(lambda x: x ** k,
                            lambda x, y: k * x ** (k - 1))

    def tanh(self):
        return self._unaria(math.tanh, lambda x, y: 1 - y * y)

    def relu(self):
        return self._unaria(lambda x: max(0.0, x),
                            lambda x, y: float(x > 0))

    def backward(self):
        """Ordena o grafo e passa os gradientes para trás."""
        ordem, visto = [], set()

        def visita(v):
            if v not in visto:
                visto.add(v)
                for f in v._filhos:
                    visita(f)
                ordem.append(v)        # depois dos filhos
        visita(self)
        self.grad = 1.0
        for v in reversed(ordem):
            v._volta()

    def __neg__(self): return self * -1
    def __sub__(self, o): return self + (-Valor._v(o))
    def __truediv__(self, o): return self * Valor._v(o) ** -1
    def __radd__(self, o): return self + o
    def __rmul__(self, o): return self * o
    def __rsub__(self, o): return Valor._v(o) - self
