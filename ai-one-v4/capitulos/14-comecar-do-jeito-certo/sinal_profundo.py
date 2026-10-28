import matplotlib.pyplot as plt

from numpy_mlp.camadas import ReLU, Rede
from numpy_mlp.dados import mnist_vetores

_, (Xv, _), _ = mnist_vetores()
fig, eixos = plt.subplots(1, 4, figsize=(10, 2.4), sharey=True)
print("início   desvio da saída das camadas 1, 3, 5, 7 e 9")
INICIOS = ["pequena", "um", "xavier", "he"]
for ax, inicio in zip(eixos, INICIOS):
    rede = Rede([784] + [100] * 9 + [10], inicio=inicio)
    A, desvios = Xv[:1000], []
    for camada in rede.camadas:
        A = camada.frente(A)
        if isinstance(camada, ReLU):
            desvios.append(A.std())
    linha = "  ".join(f"{d:8.1e}" for d in desvios[::2])
    print(f"{inicio:8} {linha}")
    ax.semilogy(range(1, 10), desvios, marker="o")
    ax.set_title(inicio)
    ax.set_xlabel("camada")
eixos[0].set_ylabel("desvio das ativações")
fig.tight_layout()
fig.savefig("sinal.png", dpi=300)
