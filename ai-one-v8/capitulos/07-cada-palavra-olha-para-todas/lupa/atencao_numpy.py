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


def softmax_vjp(p, dp):
    """O gradiente que volta pela softmax: dado dL/dp, devolve
    dL/dz = p ⊙ (dp − Σ p·dp), sem montar a Jacobiana."""
    return p * (dp - (p * dp).sum(axis=-1, keepdims=True))


def atencao_backward(Q, K, V, pesos, dO):
    """Os gradientes de Q, K e V, dado dL/dO."""
    d = Q.shape[-1]
    dV = pesos.swapaxes(-1, -2) @ dO        # Pᵀ dO
    dP = dO @ V.swapaxes(-1, -2)            # dO Vᵀ
    dS = softmax_vjp(pesos, dP)             # pela softmax
    dQ = dS @ K / np.sqrt(d)
    dK = dS.swapaxes(-1, -2) @ Q / np.sqrt(d)
    return dQ, dK, dV


def causal(T):
    """A máscara causal: True acima da diagonal, o futuro."""
    return np.triu(np.ones((T, T), dtype=bool), k=1)
