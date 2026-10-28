import matplotlib.pyplot as plt
import torch

from lupa.posicao import frequencias, senoidal

T, d = 128, 64
pe = senoidal(T, d)
w = frequencias(d)

# PE(t + k) é uma rotação de PE(t), igual para todo t
t, k = 10, 7
R = torch.zeros(d, d)
for i, wi in enumerate(w):
    c, s = torch.cos(k * wi), torch.sin(k * wi)
    R[2 * i:2 * i + 2, 2 * i:2 * i + 2] = torch.tensor(
        [[c, s], [-s, c]])
print("PE(t+k) = R(k) PE(t):",
      f"{(pe[t + k] - R @ pe[t]).abs().max():.1e}")

# o produto escalar só depende de t - s
G = pe @ pe.T
diagonais = [G.diagonal(j) for j in range(5)]
print("desvio dentro de cada diagonal:",
      " ".join(f"{dg.std():.0e}" for dg in diagonais))
print("PE(t)·PE(t+j), j = 0..5:",
      " ".join(f"{G[0, j]:.2f}" for j in range(6)))
print("comprimentos de onda: de", f"{2 * torch.pi / w[0]:.1f}",
      "a", f"{2 * torch.pi / w[-1]:.0f} posições")

fig, (a, b) = plt.subplots(1, 2, figsize=(7.5, 3))
a.imshow(pe.T, cmap="RdBu", aspect="auto")
a.set_xlabel("posição t")
a.set_ylabel("dimensão")
b.plot(G[0].numpy())
b.set_xlabel("distância t − s")
b.set_ylabel("PE(t) · PE(s)")
fig.tight_layout()
fig.savefig("ondas.png", dpi=300)
