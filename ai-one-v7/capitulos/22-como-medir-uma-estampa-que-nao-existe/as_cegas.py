import torch

from lauber.acervo import carrega, grade, partes
from lauber.dcgan import CODIGO, Gerador, desenha

imgs, _ = carrega()
_, _, teste = partes(len(imgs))
gerador = Gerador()
gerador.load_state_dict(torch.load("dcgan.pt"))
sorteio = torch.Generator().manual_seed(7)
reais = imgs[teste][torch.randperm(len(teste),
                                   generator=sorteio)[:8]]
falsas = desenha(gerador, torch.randn(8, CODIGO,
                                      generator=sorteio))
ordem = torch.randperm(16, generator=sorteio)
todas = torch.cat([reais, falsas])[ordem]
grade(todas, "as_cegas.png", colunas=8)
with open("gabarito.txt", "w") as arquivo:
    for posicao, k in enumerate(ordem.tolist(), start=1):
        lado = "real" if k < 8 else "gerada"
        arquivo.write(f"{posicao:2d} {lado}\n")
print("16 estampas em as_cegas.png, numeradas da esquerda")
print("para a direita e de cima para baixo; o gabarito está")
print("em gabarito.txt: abra só depois dos palpites.")
