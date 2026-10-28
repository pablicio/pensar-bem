import numpy as np

from lupa.atencao_numpy import softmax

rng = np.random.default_rng(0)
T, d = 5, 3
X = rng.normal(size=(T, d))      # 5 tokens de 3 números

# versão 1: dois laços
m1 = np.zeros((T, d))
for t in range(T):
    for s in range(t + 1):
        m1[t] += X[s]
    m1[t] /= t + 1

# versão 2: uma matriz triangular, com linhas que somam 1
W = np.tril(np.ones((T, T)))
W = W / W.sum(axis=1, keepdims=True)
m2 = W @ X

# versão 3: notas zero, o futuro em -inf, e a softmax
notas = np.zeros((T, T))
futuro = np.triu(np.ones((T, T), dtype=bool), k=1)
notas[futuro] = -np.inf
m3 = softmax(notas) @ X

np.set_printoptions(precision=3, suppress=True)
print(W)
print("iguais:", np.allclose(m1, m2), np.allclose(m2, m3))
