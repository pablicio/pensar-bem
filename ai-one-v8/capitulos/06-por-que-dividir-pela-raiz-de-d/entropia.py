import numpy as np

from lupa.atencao_numpy import softmax, softmax_vjp

rng = np.random.default_rng(0)
m, N = 64, 2000                 # 64 chaves, 2000 consultas
print("     d       entropia (bits)       norma de dS")
print("          sem √d     com √d     sem √d     com √d")
for d in [4, 16, 64, 256, 1024]:
    Q = rng.normal(size=(N, d))
    K = rng.normal(size=(m, d))
    dP = rng.normal(size=(N, m))      # um gradiente qualquer
    linha = []
    for divisor in [1.0, np.sqrt(d)]:
        P = softmax(Q @ K.T / divisor)
        H = -(P * np.log2(P + 1e-300)).sum(axis=1).mean()
        g = np.linalg.norm(softmax_vjp(P, dP), axis=1).mean()
        linha.append((H, g))
    (h1, g1), (h2, g2) = linha
    print(f"{d:6} {h1:10.2f} {h2:10.2f} {g1:10.2e} {g2:10.2e}")
print(f"máximo: log2({m}) = {np.log2(m):.0f} bits")
