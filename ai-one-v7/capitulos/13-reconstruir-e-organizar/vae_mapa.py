import matplotlib.pyplot as plt
import torch
from matplotlib.patches import Circle

from lauber.acervo import FAMILIAS, carrega, partes
from lauber.vae import VAE, treina_vae

torch.manual_seed(0)
imgs, info = carrega()
treino, _, teste = partes(len(imgs))
rede = VAE(codigo=2)
historico = treina_vae(rede, imgs[treino], epocas=10)
print("época  reconstrução    KL")
for epoca, (rec, k) in enumerate(historico, start=1):
    print(f"{epoca:5d} {rec:13.1f} {k:6.2f}")
rede.eval()
with torch.no_grad():
    mu, logvar = rede.codifica(imgs[teste])
    rec = rede.decodificador(mu)
    pixel = ((rec - imgs[teste]) ** 2).mean()
sigma = torch.exp(0.5 * logvar)
print(f"erro por pixel {pixel:.4f}, raio médio"
      f" {sigma.mean():.2f}, espalhamento"
      f" {mu.std(dim=0).mean():.2f}")
# das amostras de N(0, 1), quantas caem em alguma nuvem
amostras = torch.randn(2000, 2)
dist = torch.cdist(amostras, mu) / sigma.mean(dim=1)
cobertas = (dist.min(dim=1).values < 2).float().mean()
print(f"cobertura: {cobertas:.0%} das amostras de N(0, 1)")

fig, eixos = plt.subplot_mosaic([["rec", "mapa"],
                                 ["kl", "mapa"]],
                                figsize=(8, 4))
epocas = range(1, len(historico) + 1)
eixos["rec"].plot(epocas, [r for r, _ in historico])
eixos["rec"].set_ylabel("reconstrução")
eixos["kl"].plot(epocas, [k for _, k in historico], "C1")
eixos["kl"].set_ylabel("KL")
eixos["kl"].set_xlabel("época")
mapa = eixos["mapa"]
familia = info["familia"][teste]
for k, nome in enumerate(FAMILIAS):
    mapa.scatter(*mu[familia == k].T, s=2, label=nome)
for (x, y), (sx, sy) in zip(mu[:60], sigma[:60]):
    raio = float((sx + sy) / 2)
    mapa.add_patch(Circle((x, y), raio, fill=False, lw=0.4,
                          color="k"))
mapa.set_aspect("equal")
mapa.legend(markerscale=4, fontsize=6)
fig.tight_layout()
fig.savefig("vae_mapa.png", dpi=300)
