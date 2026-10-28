import csv

import matplotlib.pyplot as plt
from PIL import Image

with open("dados/brutos/fotos.csv", encoding="utf-8") as f:
    fotos = list(csv.DictReader(f))
CLASSES = ["sadia", "ferrugem", "cercosporiose",
           "bicho-mineiro", "phoma", "sol"]
fig, eixos = plt.subplots(2, 6, figsize=(9, 3.4))
for j, classe in enumerate(CLASSES):
    da_classe = [f for f in fotos if f["verdade"] == classe]
    for i in range(2):
        numero = int(da_classe[i]["foto"])
        caminho = f"dados/brutos/fotos/{numero:06d}.jpg"
        img = Image.open(caminho)
        eixos[i, j].imshow(img)
        eixos[i, j].axis("off")
    eixos[0, j].set_title(classe, fontsize=9)
fig.tight_layout()
fig.savefig("classes.png", dpi=300)
