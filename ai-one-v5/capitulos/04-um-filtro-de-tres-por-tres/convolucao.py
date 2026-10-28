import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import signal

from folha.convolucao import correlaciona

foto = Image.open("dados/brutos/fotos/000011.jpg")
cinza = np.array(foto.convert("L"), float)       # 256 × 256
cinza = cinza[20:236, 60:196]                    # só a folha
NUCLEOS = {
    "média": np.full((3, 3), 1 / 9),
    "nitidez": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
    "Sobel x": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
    "Sobel y": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
}
saidas = {}
for nome, k in NUCLEOS.items():
    saidas[nome] = correlaciona(cinza, k)
    scipy = signal.correlate2d(cinza, k, mode="valid")
    dif = np.abs(saidas[nome] - scipy).max()
    print(f"{nome:8} saída {saidas[nome].shape},"
          f" diferença do SciPy {dif:.1e}")
borda = np.hypot(saidas["Sobel x"], saidas["Sobel y"])

fig, eixos = plt.subplots(1, 5, figsize=(10, 2.4))
paineis = [("cinza", cinza), ("média", saidas["média"]),
           ("nitidez", saidas["nitidez"]),
           ("Sobel x", saidas["Sobel x"]), ("borda", borda)]
for ax, (nome, img) in zip(eixos, paineis):
    ax.imshow(img, cmap="gray")
    ax.set_title(nome)
    ax.axis("off")
fig.tight_layout()
fig.savefig("nucleos.png", dpi=300)
