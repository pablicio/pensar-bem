import matplotlib.pyplot as plt
import torch

from folha.treino import lotes
from folha.unet import Mascaras, UNet

ESCALA = [0, 1, 3, 6, 12, 25, 50]    # % da escala diagramática


def severidade(m):
    """Fração da folha coberta de lesão, foto a foto."""
    lesao = (m == 2).flatten(1).sum(dim=1).float()
    folha = (m > 0).flatten(1).sum(dim=1).float()
    return 100 * lesao / folha


def nota(s):
    """O desenho da escala mais próximo de cada severidade."""
    escala = torch.tensor(ESCALA, dtype=torch.float)
    return (s[:, None] - escala).abs().argmin(dim=1)


valid = Mascaras("validacao")
rede = UNet()
rede.load_state_dict(torch.load("unet.pt"))
rede.eval()
with torch.no_grad():
    prevista = torch.cat([rede(x).argmax(dim=1)
                          for x, _ in lotes(valid, 32)])
certa = severidade(valid.mascaras)
calculada = severidade(prevista)
erro = (calculada - certa).abs()
print(f"severidade média: certa {certa.mean():.2f}%,"
      f" calculada {calculada.mean():.2f}%")
print(f"erro médio: {erro.mean():.2f} pontos;"
      f" maior erro: {erro.max():.2f} pontos")
mesma = (nota(certa) == nota(calculada)).float().mean()
vizinha = ((nota(certa) - nota(calculada)).abs() <= 1).float()
print(f"mesma nota da escala: {mesma:.1%};"
      f" no máximo uma de distância: {vizinha.mean():.1%}")

fig, ax = plt.subplots(figsize=(4.2, 4))
ax.scatter(certa, calculada, s=8)
lim = max(certa.max(), calculada.max()).item() * 1.05
ax.plot([0, lim], [0, lim], color="gray", ls="--")
ax.set_xlabel("severidade certa (%)")
ax.set_ylabel("severidade pela U-Net (%)")
fig.tight_layout()
fig.savefig("severidade.png", dpi=400)
