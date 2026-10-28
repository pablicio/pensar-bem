import matplotlib.pyplot as plt
import torch
from matplotlib.patches import Circle

from lauber.acervo import FAMILIAS, carrega, partes
from lauber.autoencoder import Denso, treina


class Nuvem(Denso):
    """O Denso de dois números, com ruído no código no treino:
    cada estampa vira uma nuvem de raio sigma."""

    def __init__(self, sigma):
        super().__init__(codigo=2)
        self.sigma = sigma

    def forward(self, x):
        z = self.codificador(x)
        if self.training:
            z = z + self.sigma * torch.randn_like(z)
        return self.decodificador(z)


imgs, info = carrega()
treino, _, teste = partes(len(imgs))
fig, eixos = plt.subplots(1, 2, figsize=(8, 4))
print("sigma  erro  espalhamento  ruído relativo  buracos")
for eixo, sigma in zip(eixos, (0.0, 0.5)):
    torch.manual_seed(0)
    rede = Nuvem(sigma)
    historico = treina(rede, imgs[treino], epocas=10)
    rede.eval()
    with torch.no_grad():
        z = rede.codificador(imgs[teste])
    espalha = float(z.std(dim=0).mean())
    lo, hi = z.min(dim=0).values, z.max(dim=0).values
    t = torch.linspace(0, 1, 8)
    grade = torch.stack(torch.meshgrid(t, t, indexing="xy"),
                        dim=-1)
    pontos = lo + grade.view(-1, 2) * (hi - lo)
    longe = torch.cdist(pontos, z).min(dim=1).values
    buracos = int((longe > 0.1 * (hi - lo).norm()).sum())
    print(f"{sigma:5.1f} {historico[-1]:.4f} {espalha:13.2f}"
          f" {sigma / espalha:15.2f} {buracos:8d} de 64")
    familia = info["familia"][teste]
    for k, nome in enumerate(FAMILIAS):
        eixo.scatter(*z[familia == k].T, s=2, label=nome)
    raio = max(sigma, 0.02)
    for x, y in z[:60]:            # as nuvens de 60 estampas
        eixo.add_patch(Circle((x, y), raio, fill=False, lw=0.4,
                              color="k"))
    eixo.set_title(f"sigma = {sigma}", fontsize=9)
    eixo.set_aspect("equal")
eixos[1].legend(markerscale=4, fontsize=6)
fig.tight_layout()
fig.savefig("nuvens.png", dpi=300)
