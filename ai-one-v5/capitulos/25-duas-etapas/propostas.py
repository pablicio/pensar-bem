import matplotlib.pyplot as plt
import torch
from matplotlib.patches import Rectangle

from folha.duas_etapas import detecta, exemplos, faster

rede = faster(512)
rede.load_state_dict(torch.load("faster_512.pt"))
rede.eval()
valid = exemplos("validacao")
# a foto de bicho-mineiro com mais minas na validação
minas = [(a["labels"] == 3).sum() for _, a in valid]
x, alvo = valid[max(range(len(valid)), key=lambda i: minas[i])]

with torch.no_grad():
    imagens, _ = rede.transform([x])          # 256 → 512
    mapas = rede.backbone(imagens.tensors)    # pirâmide (FPN)
    propostas, _ = rede.rpn(imagens, mapas)   # 1ª etapa
escala = 256 / 512
print("mapas da pirâmide:",
      {k: tuple(v.shape[-2:]) for k, v in mapas.items()})
print(f"propostas da RPN: {len(propostas[0])}")
caixas, notas, _ = detecta(rede, x)           # 2ª etapa
print(f"caixas finais acima de 0,5: {(notas > 0.5).sum()};"
      f" lesões na foto: {len(alvo['boxes'])}")

fig, eixos = plt.subplots(1, 2, figsize=(6, 3.2))
QUADROS = [(eixos[0], "30 primeiras propostas",
            propostas[0][:30] * escala, "cyan"),
           (eixos[1], "caixas finais", caixas[notas > 0.5],
            "yellow")]
for ax, titulo, lista, cor in QUADROS:
    ax.imshow(x.permute(1, 2, 0))
    for c in lista:
        ax.add_patch(Rectangle(c[:2], *(c[2:] - c[:2]),
                               fill=False, ec=cor, lw=0.7))
    ax.set_title(titulo, fontsize=9)
    ax.axis("off")
fig.tight_layout()
fig.savefig("propostas.png", dpi=300)
