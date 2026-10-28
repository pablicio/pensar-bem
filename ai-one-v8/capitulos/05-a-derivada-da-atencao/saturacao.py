import numpy as np

from lupa.atencao_numpy import softmax

z = np.array([0.0, 1.0, 1.0, 2.0])
print("  escala   maior peso   norma de J")
for c in [1, 4, 16, 64]:
    p = softmax(c * z)
    J = np.diag(p) - np.outer(p, p)
    print(f"{c:8} {p.max():12.6f} {np.linalg.norm(J):12.2e}")
