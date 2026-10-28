import matplotlib.pyplot as plt

from leitora.carrega import leitora, probabilidades
from leitora.dados import CaixasDoCartao

valid = CaixasDoCartao("validacao")
p = probabilidades(leitora(), valid.imagens)
confianca, previsto = p.max(dim=1)
erros = (previsto != valid.rotulos).nonzero().flatten()
piores = erros[confianca[erros].argsort(descending=True)][:12]

print("inscrição questão caixa  era  leu  certeza")
fig, eixos = plt.subplots(2, 6, figsize=(9, 3.6))
for ax, i in zip(eixos.flat, piores.tolist()):
    insc, q, k = (int(v) for v in valid.origem[i])
    era, leu = valid.rotulos[i].item(), previsto[i].item()
    print(f"{insc:9} {q + 1:7} {k + 1:5} {era:4} {leu:4}"
          f" {confianca[i]:8.1%}")
    ax.imshow(valid.imagens[i], cmap="gray_r")
    ax.set_title(f"era {era}, leu {leu}", fontsize=9)
    ax.axis("off")
fig.tight_layout()
fig.savefig("galeria.png", dpi=300)

# e o cartão da Valentina, inscrição 31877
print()
print("os erros no cartão da Valentina:")
for i in erros.tolist():
    insc, q, k = (int(v) for v in valid.origem[i])
    if insc == 31_877:
        era, leu = valid.rotulos[i].item(), previsto[i].item()
        print(f"  questão {q + 1}, caixa {k + 1}: era {era},"
              f" leu {leu}, com {confianca[i]:.1%}")
