import numpy as np
import torch
from PIL import Image
from torchvision.transforms import v2

from folha.conjunto import CLASSES, PASTA, parte, tabela

torch.manual_seed(0)
fotos = [f for f in tabela() if parte(f["fazenda"]) == "treino"
         and f["verdade"] != "sadia"]
print("fotos doentes no treino:", len(fotos))
ESCALAS = [(0.08, 1.0), (0.5, 1.0)]
vazios = {c: [0, 0] for c in CLASSES[1:]}
for k, escala in enumerate(ESCALAS):
    for f in fotos:
        nome = f"{int(f['foto']):06d}.png"
        mascara = Image.open(PASTA / "mascaras" / nome)
        mascara = np.array(mascara)
        for _ in range(10):
            i, j, h, w = v2.RandomResizedCrop.get_params(
                torch.zeros(1, 256, 256), escala,
                (3 / 4, 4 / 3))
            sem = not (mascara[i:i + h, j:j + w] == 2).any()
            vazios[f["verdade"]][k] += sem
print("recortes sem lesão  área ≥ 8%  área ≥ 50%")
for classe, (pequeno, grande) in vazios.items():
    n = 10 * sum(f["verdade"] == classe for f in fotos)
    print(f"{classe:18} {pequeno / n:9.0%} {grande / n:11.0%}")
