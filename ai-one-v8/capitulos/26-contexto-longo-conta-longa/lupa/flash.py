"""A atenção em blocos, sem guardar a matriz T x T."""
import numpy as np


def softmax_online(z, bloco):
    """A softmax lendo z aos pedaços: o máximo e a soma das
    exponenciais são corrigidos a cada pedaço novo."""
    m, l = -np.inf, 0.0
    for i in range(0, len(z), bloco):
        pedaco = z[i:i + bloco]
        m_novo = max(m, pedaco.max())
        soma = np.exp(pedaco - m_novo).sum()
        l = l * np.exp(m - m_novo) + soma
        m = m_novo
    return np.exp(z - m) / l


def atencao_em_blocos(Q, K, V, bloco=128):
    """O mesmo que softmax(Q Kᵀ / √d) V, guardando só notas de
    (n, bloco) de cada vez."""
    n, d = Q.shape
    m = np.full((n, 1), -np.inf)       # o máximo de cada linha
    l = np.zeros((n, 1))               # soma das exponenciais
    o = np.zeros((n, V.shape[1]))      # a saída, sem dividir
    for j in range(0, len(K), bloco):
        s = Q @ K[j:j + bloco].T / np.sqrt(d)     # (n, bloco)
        m_novo = np.maximum(m, s.max(1, keepdims=True))
        corr = np.exp(m - m_novo)      # corrige o que já foi
        p = np.exp(s - m_novo)
        l = l * corr + p.sum(1, keepdims=True)
        o = o * corr + p @ V[j:j + bloco]
        m = m_novo
    return o / l
