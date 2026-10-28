import csv

import numpy as np
from PIL import Image

with open("dados/brutos/fotos.csv", encoding="utf-8") as f:
    fotos = list(csv.DictReader(f))
print(len(fotos), "fotos; a primeira:")
for chave, valor in fotos[0].items():
    print(f"  {chave:10} {valor}")

foto = np.asarray(Image.open("dados/brutos/fotos/000001.jpg"))
print("formato:", foto.shape, foto.dtype)
print("o pixel do meio:", foto[128, 128])
