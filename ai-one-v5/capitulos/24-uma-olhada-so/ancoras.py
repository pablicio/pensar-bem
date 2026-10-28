import torch

from folha.conjunto import Folhas
from folha.yolo import caixas_com_tipo, iou_formas, kmeans

todas = caixas_com_tipo()
treino = Folhas("treino", lado=32)   # só as linhas importam
caixas = [todas[f["foto"]] for f in treino.linhas
          if f["foto"] in todas]
formas = torch.cat([c[:, 2:4] - c[:, :2] for c in caixas])
print(f"{len(formas)} lesões no treino")
for k in (1, 2, 3, 5):
    ancoras = kmeans(formas, k)
    melhor = iou_formas(formas, ancoras).max(dim=1).values
    lista = ", ".join(f"{l:.0f}×{h:.0f}" for l, h in ancoras)
    print(f"k = {k}: IoU média {melhor.mean():.3f}"
          f"  âncoras {lista}")
torch.save(kmeans(formas, 3), "ancoras.pt")
