import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader

from leitora.dados import MNIST, CaixasDoCartao

for parte in ["treino", "validacao", "teste"]:
    n = len(CaixasDoCartao(parte))
    print(f"caixas escritas, {parte}: {n:,}")
print(f"MNIST, treino: {len(MNIST('treino')):,}")

caixas = CaixasDoCartao("treino")
torch.manual_seed(0)
lotes = DataLoader(caixas, batch_size=64, shuffle=True)
x, y = next(iter(lotes))
print(f"imagens de um lote: {tuple(x.shape)} {x.dtype}")
print(f"rótulos de um lote: {tuple(y.shape)} {y.dtype}")
print(f"{len(lotes)} lotes por época")

fig, eixos = plt.subplots(4, 8, figsize=(8, 4.4))
for ax, img, r in zip(eixos.flat, x, y):
    ax.imshow(img, cmap="gray_r")
    ax.set_title(str(r.item()), fontsize=9)
    ax.axis("off")
fig.tight_layout()
fig.savefig("lote.png", dpi=300)
