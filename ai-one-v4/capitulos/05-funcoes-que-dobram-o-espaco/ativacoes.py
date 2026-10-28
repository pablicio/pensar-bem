import matplotlib.pyplot as plt
import numpy as np


def sigmoide(z):
    return 1 / (1 + np.exp(-z))


def relu(z):
    return np.maximum(0, z)


FUNCOES = {"sigmoide": sigmoide, "tanh": np.tanh, "ReLU": relu}

if __name__ == "__main__":
    z = np.array([-4.0, -1.0, 0.0, 1.0, 4.0])
    print("z:       ", z)
    for nome, f in FUNCOES.items():
        print(f"{nome:9}", f(z).round(3))

    zz = np.linspace(-5, 5, 401)
    fig, eixos = plt.subplots(1, 3, figsize=(9, 2.8),
                              sharey=True)
    for ax, (nome, f) in zip(eixos, FUNCOES.items()):
        ax.plot(zz, f(zz))
        ax.axhline(0, color="gray", lw=0.5)
        ax.axvline(0, color="gray", lw=0.5)
        ax.set_title(nome)
        ax.set_ylim(-1.3, 2.3)
    fig.tight_layout()
    fig.savefig("ativacoes.png", dpi=300)
