import matplotlib.pyplot as plt

from casinha import CASINHA
from matriz import matriz_vezes_vetor, multiplicar

R = [[0, -1], [1, 0]]        # gira 90 graus no anti-horário
S = [[2, 0], [0, 1]]         # estica 2 vezes na horizontal
I = [[1, 0], [0, 1]]         # a identidade: não muda nada

SR = multiplicar(S, R)       # primeiro R, depois S
RS = multiplicar(R, S)       # primeiro S, depois R
print("S R =", SR)
print("R S =", RS)

plt.figure(figsize=(9, 3.4))
for posicao, M, titulo in [(1, I, "original"),
                           (2, SR, "gira, depois estica"),
                           (3, RS, "estica, depois gira")]:
    plt.subplot(1, 3, posicao)
    xs = []
    ys = []
    for ponto in CASINHA:
        x, y = matriz_vezes_vetor(M, ponto)
        xs.append(x)
        ys.append(y)
    plt.plot(xs, ys, marker="o", markersize=3)
    plt.xlim(-3.5, 3.5)
    plt.ylim(-3.5, 3.5)
    plt.gca().set_aspect("equal")
    plt.title(titulo)
plt.savefig("transformacoes.png", dpi=300, bbox_inches="tight")
