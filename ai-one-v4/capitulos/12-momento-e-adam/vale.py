import matplotlib.pyplot as plt
import numpy as np


def grad(p):
    """f(x, y) = x²/2 + 10 y²: um vale estreito e comprido."""
    return np.array([p[0], 20 * p[1]])


def caminho(metodo, passos=60):
    p = np.array([-9.0, 1.0])
    v, m, s = np.zeros(2), np.zeros(2), np.zeros(2)
    pontos = [p.copy()]
    for t in range(1, passos + 1):
        g = grad(p)
        if metodo == "SGD":
            p -= 0.09 * g
        elif metodo == "momento":
            v = 0.8 * v + g
            p -= 0.03 * v
        else:                                   # Adam
            m = 0.9 * m + 0.1 * g
            s = 0.999 * s + 0.001 * g * g
            mh, sh = m / (1 - 0.9**t), s / (1 - 0.999**t)
            p -= 0.5 * mh / (np.sqrt(sh) + 1e-8)
        pontos.append(p.copy())
    return np.array(pontos)


fig, ax = plt.subplots(figsize=(8, 3))
xx, yy = np.meshgrid(np.linspace(-10, 2, 200),
                     np.linspace(-1.5, 1.5, 100))
ax.contour(xx, yy, xx**2 / 2 + 10 * yy**2, levels=15,
           colors="lightgray")
for nome in ["SGD", "momento", "Adam"]:
    c = caminho(nome)
    ax.plot(c[:, 0], c[:, 1], marker=".", ms=3, label=nome)
    print(f"{nome:8} depois de 60 passos: ({c[-1, 0]:.3f},"
          f" {c[-1, 1]:.3f})")
ax.legend()
fig.tight_layout()
fig.savefig("vale.png", dpi=300)
