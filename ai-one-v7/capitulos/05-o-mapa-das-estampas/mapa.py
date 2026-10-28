import matplotlib.pyplot as plt
import torch

from lauber.acervo import FAMILIAS, carrega, grade, partes
from lauber.autoencoder import Denso, treina

torch.manual_seed(0)
imgs, info = carrega()
treino, _, teste = partes(len(imgs))
rede = Denso(codigo=2)
treina(rede, imgs[treino], epocas=10)
torch.save(rede.state_dict(), "mapa.pt")
with torch.no_grad():
    z = rede.codificador(imgs[teste])
    rosa, xadrez = rede.codificador(imgs[:2])  # índices 0 e 1
fig, ax = plt.subplots(figsize=(6, 5))
familia = info["familia"][teste]
for k, nome in enumerate(FAMILIAS):
    ax.scatter(*z[familia == k].T, s=3, label=nome)
ax.plot(*torch.stack([rosa, xadrez]).T, "k--", lw=1)
ax.annotate("Rosa 1964", rosa, fontsize=8)
ax.annotate("Xadrez 1971", xadrez, fontsize=8)
ax.legend(markerscale=4, fontsize=7)
fig.tight_layout()
fig.savefig("mapa.png", dpi=300)
# uma grade de 8 x 8 pontos do plano, decodificados
lo, hi = z.min(dim=0).values, z.max(dim=0).values
t = torch.linspace(0, 1, 8)
pontos = torch.stack(torch.meshgrid(t, t, indexing="xy"), -1)
pontos = lo + pontos.view(-1, 2) * (hi - lo)
with torch.no_grad():
    grade(rede.decodificador(pontos.flip(0)), "plano.png", 8)
# da Rosa ao Xadrez em oito passos: pelos pixels, pelo
# código de 2 números e pelo de um autoencoder de 16
torch.manual_seed(0)
rede16 = Denso(codigo=16)
treina(rede16, imgs[treino], epocas=10)
a = torch.linspace(0, 1, 8)[:, None]
caminhos = [(1 - a[..., None, None]) * imgs[0]
            + a[..., None, None] * imgs[1]]
with torch.no_grad():
    for r in (rede, rede16):
        z0, z1 = r.codificador(imgs[:2])
        caminhos.append(r.decodificador((1 - a) * z0 + a * z1))
grade(torch.cat(caminhos), "interpola.png", 8)
dist = torch.cdist(pontos, z).min(dim=1).values
print(f"códigos do teste: x de {lo[0]:.1f} a {hi[0]:.1f},"
      f" y de {lo[1]:.1f} a {hi[1]:.1f}")
print(f"pontos da grade longe de qualquer estampa: "
      f"{(dist > 0.1 * (hi - lo).norm()).sum()} de 64")
