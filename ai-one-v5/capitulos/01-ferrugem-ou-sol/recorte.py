import numpy as np
from PIL import Image

foto = np.array(Image.open("dados/brutos/fotos/000068.jpg"))
caminho = "dados/brutos/mascaras/000068.png"
mascara = np.array(Image.open(caminho))
y, x = 153, 162                  # a borda de uma pústula
for c, nome in enumerate(["vermelho", "verde", "azul"]):
    print(nome)
    print(foto[y:y + 6, x:x + 6, c])
print("máscara (1 folha, 2 lesão)")
print(mascara[y:y + 6, x:x + 6])
