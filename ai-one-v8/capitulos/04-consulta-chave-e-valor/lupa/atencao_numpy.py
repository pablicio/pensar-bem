"""A atenção em NumPy: a conta do Transformer, à vista."""
import numpy as np


def softmax(z, eixo=-1):
    """Softmax estável: subtrai o máximo antes da exponencial,
    o que não muda o resultado e evita o estouro."""
    z = z - z.max(axis=eixo, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=eixo, keepdims=True)


def atencao(Q, K, V, mascara=None):
    """softmax(Q Kᵀ / √d) V. Q: (n, d), K: (m, d), V: (m, dv).
    mascara: (n, m), True onde a consulta não pode olhar."""
    d = Q.shape[-1]
    notas = Q @ K.swapaxes(-1, -2) / np.sqrt(d)
    if mascara is not None:
        notas = np.where(mascara, -np.inf, notas)
    pesos = softmax(notas)
    return pesos @ V, pesos
