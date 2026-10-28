import matplotlib.pyplot as plt

from folha.emprestada import extratora

rede = extratora()
filtros = rede[1].conv1.weight.detach()
print("primeira camada:", tuple(filtros.shape))
fig, eixos = plt.subplots(4, 16, figsize=(8, 2.2))
for ax, f in zip(eixos.flat, filtros):
    f = (f - f.min()) / (f.max() - f.min())      # para 0..1
    ax.imshow(f.permute(1, 2, 0))
    ax.axis("off")
fig.tight_layout(pad=0.2)
fig.savefig("filtros_imagenet.png", dpi=300)
