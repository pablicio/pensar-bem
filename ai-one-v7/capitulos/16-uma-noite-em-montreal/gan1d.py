import matplotlib.pyplot as plt
import torch
from torch import nn


def larguras(n):
    """Larguras de listra dos cadernos da Zuleica, em mm:
    60% finas, perto de 3, e 40% largas, perto de 8."""
    fina = torch.rand(n, 1) < 0.6
    return torch.where(fina, 3 + 0.5 * torch.randn(n, 1),
                       8 + 1.0 * torch.randn(n, 1))


def rede():
    return nn.Sequential(nn.Linear(1, 32), nn.ReLU(),
                         nn.Linear(32, 32), nn.ReLU(),
                         nn.Linear(32, 1))


def distancia(a, b):
    """A diferença média entre os quantis das amostras."""
    return (a.sort(0).values - b.sort(0).values).abs().mean()


torch.manual_seed(0)
gerador, perito = rede(), rede()
otimo_g = torch.optim.Adam(gerador.parameters(), lr=1e-3)
otimo_p = torch.optim.Adam(perito.parameters(), lr=1e-3)
bce = nn.BCEWithLogitsLoss()
verdade, mentira = torch.ones(256, 1), torch.zeros(256, 1)
alvo = larguras(5000)
fotos = {}
for passo in range(8001):
    if passo in (0, 500, 2000, 8000):
        with torch.no_grad():
            fotos[passo] = gerador(torch.randn(5000, 1))
    # o perito aprende a separar as larguras reais das falsas
    real = larguras(256)
    falsa = gerador(torch.randn(256, 1))
    perda_p = (bce(perito(real), verdade)
               + bce(perito(falsa.detach()), mentira))
    otimo_p.zero_grad()
    perda_p.backward()
    otimo_p.step()
    # o gerador aprende a fazer o perito dizer "real"
    perda_g = bce(perito(falsa), verdade)
    otimo_g.zero_grad()
    perda_g.backward()
    otimo_g.step()
print("passo  média  finas  largas  distância")
for passo, x in [*fotos.items(), ("alvo", alvo)]:
    finas = (x < 5.5).float().mean()
    print(f"{passo:>5} {x.mean():6.2f} {finas:6.0%}"
          f" {1 - finas:7.0%} {distancia(x, alvo):10.2f}")
fig, eixos = plt.subplots(1, 4, figsize=(10, 2.5), sharey=True)
for eixo, (passo, x) in zip(eixos, fotos.items()):
    eixo.hist(alvo.ravel(), bins=60, range=(-2, 14),
              density=True, color="0.8")
    eixo.hist(x.ravel(), bins=60, range=(-2, 14), density=True,
              histtype="step", color="C3")
    eixo.set_title(f"passo {passo}", fontsize=9)
    eixo.set_xlabel("largura (mm)", fontsize=8)
fig.tight_layout()
fig.savefig("gan1d.png", dpi=300)
