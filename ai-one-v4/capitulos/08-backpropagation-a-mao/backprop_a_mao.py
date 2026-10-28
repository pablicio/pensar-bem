import numpy as np

from perdas import entropia_cruzada, softmax

sorteio = np.random.default_rng(0)
# 2 entradas, 3 escondidos com tanh, 2 saídas com softmax
P = {"W1": sorteio.normal(size=(3, 2)),
     "b1": sorteio.normal(size=3),
     "W2": sorteio.normal(size=(2, 3)),
     "b2": sorteio.normal(size=2)}
x, y = np.array([0.5, -1.2]), 1          # um exemplo, rótulo 1


def perda(P):
    h = np.tanh(P["W1"] @ x + P["b1"])
    return entropia_cruzada(P["W2"] @ h + P["b2"], y)


# para frente, guardando os valores do meio
z1 = P["W1"] @ x + P["b1"]
h = np.tanh(z1)
z2 = P["W2"] @ h + P["b2"]
print(f"perda: {entropia_cruzada(z2, y):.6f}")

# para trás, camada por camada
G = {}
dz2 = softmax(z2) - np.eye(2)[y]        # o capítulo 6
G["W2"] = np.outer(dz2, h)
G["b2"] = dz2
dh = P["W2"].T @ dz2                    # volta pelos pesos
dz1 = dh * (1 - h**2)                   # derivada da tanh
G["W1"] = np.outer(dz1, x)
G["b1"] = dz1

# a conferência, peso por peso
eps = 1e-6
print(f"{'parâmetro':10} {'analítico':>11} {'numérico':>12}"
      f" {'dif. rel.':>11}")
for nome, valor in P.items():
    for i in np.ndindex(valor.shape):
        guarda = valor[i]
        valor[i] = guarda + eps
        mais = perda(P)
        valor[i] = guarda - eps
        menos = perda(P)
        valor[i] = guarda
        num = (mais - menos) / (2 * eps)
        a = G[nome][i]
        rel = abs(a - num) / max(abs(a), abs(num))
        rotulo = f"{nome}{list(i)}"
        print(f"{rotulo:10} {a:11.6f} {num:12.6f} {rel:11.1e}")
