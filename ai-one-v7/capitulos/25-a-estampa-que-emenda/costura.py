import torch

from lauber.acervo import carrega, grade, partes
from lauber.dcgan import CODIGO, Gerador, desenha
from lauber.emenda import costura, ladrilho

imgs, _ = carrega()
_, _, teste = partes(len(imgs))
gerador = Gerador()
gerador.load_state_dict(torch.load("dcgan.pt"))
torch.manual_seed(1)
geradas = desenha(gerador, torch.randn(500, CODIGO))
print(f"costura do acervo: {costura(imgs[teste]):.2f}")
print(f"costura da DCGAN:  {costura(geradas):.2f}")
grade(torch.stack([ladrilho(imgs[teste][3]),
                   ladrilho(geradas[0])]),
      "ladrilho_dcgan.png", colunas=2)
