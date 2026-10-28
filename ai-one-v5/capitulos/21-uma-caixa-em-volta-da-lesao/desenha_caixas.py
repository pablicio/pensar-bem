import matplotlib.pyplot as plt
import torch
from matplotlib.patches import Rectangle

from folha.caixas import do_conjunto
from folha.conjunto import DESVIO, MEDIA
from folha.localizacao import Lesoes, RedeLocal

valid = Lesoes("validacao", "maior")
todas = do_conjunto()
redes = {}
for alvo in ("maior", "uniao"):
    redes[alvo] = RedeLocal()
    redes[alvo].load_state_dict(torch.load(f"local_{alvo}.pt"))
    redes[alvo].eval()
media = torch.tensor(MEDIA).view(3, 1, 1)
desvio = torch.tensor(DESVIO).view(3, 1, 1)
# duas fotos com uma lesão e duas com muitas
uma = (valid.quantas == 1).nonzero().flatten()[:2]
muitas = (valid.quantas >= 6).nonzero().flatten()[:2]
fig, eixos = plt.subplots(1, 4, figsize=(8, 2.3))
for ax, i in zip(eixos, torch.cat([uma, muitas]).tolist()):
    x = valid[i][0]
    imagem = (x * desvio + media).clamp(0, 1)
    ax.imshow(imagem.permute(1, 2, 0))
    foto = valid.fotos.linhas[i]["foto"]
    for c in todas[foto] / 2:            # de 256 para 128
        ax.add_patch(Rectangle(c[:2], *(c[2:] - c[:2]),
                               fill=False, ec="white", lw=0.6))
    for alvo, cor in (("maior", "red"), ("uniao", "yellow")):
        with torch.no_grad():
            c = redes[alvo](x[None])[1][0] * 128
        ax.add_patch(Rectangle(c[:2], *(c[2:] - c[:2]),
                               fill=False, ec=cor, lw=1.2,
                               ls="--"))
    n = valid.quantas[i].item()
    ax.set_title("1 lesão" if n == 1 else f"{n} lesões",
                 fontsize=8)
    ax.axis("off")
fig.tight_layout()
fig.savefig("caixas.png", dpi=300)
