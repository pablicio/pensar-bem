import matplotlib.pyplot as plt

from lupa.escaneado import conjunto

x, y = conjunto(8, semente=3)
fig, eixos = plt.subplots(1, 8, figsize=(8, 1.4))
for img, d, eixo in zip(x[:, 0], y, eixos):
    eixo.imshow(img, cmap="gray", vmin=0, vmax=1)
    for k in (8, 16, 24):                    # os pedaços 8 x 8
        eixo.axhline(k - 0.5, color="tab:orange", lw=0.8)
        eixo.axvline(k - 0.5, color="tab:orange", lw=0.8)
    eixo.set_title(str(int(d)))
    eixo.axis("off")
fig.tight_layout()
fig.savefig("pedacos.png", dpi=300)
print("rótulos:", y.tolist())
