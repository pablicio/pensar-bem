import numpy as np

from lupa.atencao_numpy import softmax

np.set_printoptions(precision=4, suppress=True)
z = np.array([0.0, 1.0, 1.0, 2.0])
p = softmax(z)
J = np.diag(p) - np.outer(p, p)        # a fórmula
# a mesma Jacobiana por diferenças finitas centrais
eps = 1e-6
J_num = np.zeros((4, 4))
for j in range(4):
    e = np.zeros(4)
    e[j] = eps
    J_num[:, j] = (softmax(z + e) - softmax(z - e)) / (2 * eps)
print("J =\n", J)
print("maior diferença para a numérica:",
      f"{np.abs(J - J_num).max():.1e}")
print("soma das linhas:", J.sum(axis=1))
print("autovalores:", np.linalg.eigvalsh(J))

dp = np.array([0.3, -1.0, 0.5, 2.0])
print("Jᵀ dp:       ", J.T @ dp)
print("fórmula:     ", p * (dp - p @ dp))
