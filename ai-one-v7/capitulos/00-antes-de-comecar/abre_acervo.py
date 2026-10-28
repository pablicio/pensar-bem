import matplotlib.pyplot as plt
import numpy as np

from dados.estampas import FAMILIAS

acervo = np.load("dados/brutos/acervo.npz")
imgs = acervo["escaneada"]
print(imgs.shape, imgs.dtype, imgs.min(), imgs.max())
print("da Zuleica:", acervo["zuleica"].sum())
print("com algum dano:", (acervo["dano"] != "").sum())
for k, nome in enumerate(FAMILIAS):
    print(f"  {nome:11}", (acervo["familia"] == k).sum())
# uma grade com seis estampas de cada família
fig, eixos = plt.subplots(6, 6, figsize=(6, 6))
for k, linha in enumerate(eixos):
    escolhidas = np.flatnonzero(acervo["familia"] == k)[:6]
    for eixo, i in zip(linha, escolhidas):
        eixo.imshow(imgs[i])
        eixo.axis("off")
fig.tight_layout()
fig.savefig("acervo.png", dpi=300)
