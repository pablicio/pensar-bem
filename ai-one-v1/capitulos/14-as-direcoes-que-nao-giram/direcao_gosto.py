import matplotlib.pyplot as plt

from matriz import multiplicar, transposta
from operacoes import escalar, media, soma
from potencia import iteracao_potencia
from similaridade import produto_escalar

nomes = []
pontos = []
with open("nuvem.csv", encoding="utf-8") as arquivo:
    arquivo.readline()
    for linha in arquivo:
        campos = linha.strip().split(",")
        nomes.append(campos[0])
        pontos.append([float(campos[1]), float(campos[2])])

centro = media(pontos)
X = [soma(p, escalar(-1, centro)) for p in pontos]  # centrada
M = multiplicar(transposta(X), X)                   # 2 x 2
direcao, autovalor = iteracao_potencia(M)
print("centro:", [round(c, 3) for c in centro])
print("M:", [[round(x, 4) for x in linha] for linha in M])
print("direção dominante:", [round(d, 3) for d in direcao])
print("autovalor:", round(autovalor, 4))

projecoes = [produto_escalar(x, direcao) for x in X]
notas = sorted(zip(projecoes, nomes))
for valor, nome in notas:
    print(f"{nome:13s} {valor:+.3f}")

plt.figure(figsize=(5.5, 5.5))
plt.scatter([x[0] for x in X], [x[1] for x in X])
plt.plot([-0.5 * direcao[0], 0.5 * direcao[0]],
         [-0.5 * direcao[1], 0.5 * direcao[1]], linestyle="--")
plt.xlim(-0.5, 0.5)
plt.ylim(-0.5, 0.5)
plt.gca().set_aspect("equal")
plt.xlabel("energia (em relação à média)")
plt.ylabel("acústico (em relação à média)")
plt.savefig("direcao_gosto.png", dpi=300, bbox_inches="tight")
