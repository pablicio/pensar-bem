import numpy as np

from lupa.atencao_numpy import atencao, causal

rng = np.random.default_rng(0)
frase = "a empresa contratou o município".split()
vocab = {p: rng.normal(size=8) for p in frase}
W_Q, W_K, W_V = (rng.normal(size=(8, 8)) for _ in range(3))


def autoatencao(palavras, mascara=None):
    X = np.stack([vocab[p] for p in palavras])
    return atencao(X @ W_Q, X @ W_K, X @ W_V, mascara)[0]


trocada = "o município contratou a empresa".split()
ordem = [frase.index(p) for p in trocada]      # a permutação
A, B = autoatencao(frase), autoatencao(trocada)
print("sem máscara, B é A permutada:",
      np.allclose(B, A[ordem]))
C = autoatencao(frase, causal(5))
D = autoatencao(trocada, causal(5))
print("com a máscara causal:        ",
      np.allclose(D, C[ordem]))
print("saída de 'contratou' nas duas frases:")
print(np.round(A[2], 3))
print(np.round(B[2], 3))
