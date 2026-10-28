import matplotlib.pyplot as plt
import numpy as np

from rio.numpy_rnn import rnn, rnn_inicia

T = 60
sorteio = np.random.default_rng(1)
xs = sorteio.normal(0, 1, (T, 1))
fig, ax = plt.subplots(figsize=(6, 3.2))
print("raio    k = 10      k = 25      k = 50")
for raio in (0.5, 0.9, 1.1, 1.5):
    p = rnn_inicia(1, 16, np.random.default_rng(2))
    autovalor = np.abs(np.linalg.eigvals(p["Wh"])).max()
    p["Wh"] *= raio / autovalor    # maior autovalor = raio
    p["Wx"] *= 0.3
    estados = rnn(p, xs)
    J = np.eye(16)                     # dh_T / dh_T
    normas = [1.0]
    for t in range(T - 1, 0, -1):      # dh_T / dh_(t-1)
        J = J @ (np.diag(1 - estados[t] ** 2) @ p["Wh"])
        normas.append(np.linalg.norm(J, 2))
    ax.semilogy(normas, label=f"raio {raio}")
    print(f"{raio:4}  " + "  ".join(f"{normas[k]:10.2e}"
                                  for k in (10, 25, 50)))
ax.set_xlabel("passos para trás")
ax.set_ylabel("norma de dh_T / dh_(T-k)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("jacobiana.png", dpi=300)
