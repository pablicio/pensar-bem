import torch

from lauber.acervo import FAMILIAS, carrega, grade
from lauber.classificador import Classificador

FLORAL = FAMILIAS.index("floral")
torch.manual_seed(0)
rede = Classificador()
rede.load_state_dict(torch.load("classificador.pt"))
imgs, info = carrega()
florais = imgs[info["familia"] == FLORAL]
# 1. subir o gradiente da nota de floral, a partir do cinza
x = torch.full((1, 3, 32, 32), 0.5, requires_grad=True)
otimo = torch.optim.Adam([x], lr=0.05)
for passo in range(200):
    nota = rede(x.clamp(0, 1))
    perda = -torch.log_softmax(nota, dim=1)[0, FLORAL]
    otimo.zero_grad()
    perda.backward()
    otimo.step()
subida = x.detach().clamp(0, 1)
# 2. a média de todos os florais do acervo
media = florais.mean(dim=0, keepdim=True)
# 3. cada pixel copiado de um floral sorteado
qual = torch.randint(len(florais), (32, 32))
linha, coluna = torch.meshgrid(torch.arange(32),
                               torch.arange(32), indexing="ij")
sorteio = florais[qual, :, linha, coluna]   # (32, 32, 3)
sorteio = sorteio.permute(2, 0, 1)[None]
tentativas = torch.cat([subida, media, sorteio, florais[:1]])
with torch.no_grad():
    p = torch.softmax(rede(tentativas), dim=1)[:, FLORAL]
nomes = ["gradiente", "média", "sorteio", "do acervo"]
for nome, prob in zip(nomes, p):
    print(f"{nome:10} P(floral) = {prob:.2f}")
grade(tentativas, "tentativas.png", colunas=4, titulos=nomes)
