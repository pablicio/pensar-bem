import matplotlib.pyplot as plt
import torch

from folha.conjunto import CLASSES, DESVIO, MEDIA, Folhas
from folha.fundos import FundoTrocado
from folha.olhar import gradcam
from folha.redes import rede_global

valid = Folhas("validacao")
na_mesa = FundoTrocado("validacao", "mesa")


def primeira(dados, classe, fundo):
    """A primeira foto da classe com o fundo pedido."""
    for i, linha in enumerate(dados.linhas):
        par = (linha["verdade"], linha["fundo"])
        if par == (classe, fundo):
            return dados[i][0]


fotos = [
    ("ferrugem na mesa", primeira(valid, "ferrugem", "mesa")),
    ("sadia, mesa trocada",
     primeira(na_mesa, "sadia", "terra"))]
media = torch.tensor(MEDIA).view(3, 1, 1)
desvio = torch.tensor(DESVIO).view(3, 1, 1)
NOMES = ("sempre", "matiz", "matiz_fundos")
fig, eixos = plt.subplots(2, 4, figsize=(8, 4.3))
for linha, (titulo, x) in zip(eixos, fotos):
    imagem = (x * desvio + media).clamp(0, 1).permute(1, 2, 0)
    linha[0].imshow(imagem)
    linha[0].set_title(titulo, fontsize=8)
    for ax, nome in zip(linha[1:], NOMES):
        rede = rede_global()
        rede.load_state_dict(torch.load(f"{nome}.pt"))
        classe = rede(x[None]).argmax().item()
        mapa = gradcam(rede, rede[10], x[None])[0]
        ax.imshow(imagem)
        ax.imshow(mapa, cmap="jet", alpha=0.45)
        ax.set_title(f"{nome}: {CLASSES[classe]}", fontsize=8)
for ax in eixos.flat:
    ax.axis("off")
fig.tight_layout()
fig.savefig("gradcam.png", dpi=300)
