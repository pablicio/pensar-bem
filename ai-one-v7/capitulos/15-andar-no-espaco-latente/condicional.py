import torch

from lauber.acervo import FAMILIAS, carrega, grade, partes
from lauber.classificador import Classificador, treina
from lauber.condicional import Condicional, treina_condicional

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina(juiz, imgs[treino], familia[treino])
torch.manual_seed(1)
z = torch.randn(500, 16)        # 500 "almas", as mesmas
todas = torch.arange(6).repeat_interleave(500)
nomes = " ".join(f"{n[:6]:>6}" for n in FAMILIAS)
print(f"beta  efeito  {nomes}")
for beta in (1.0, 4.0):
    torch.manual_seed(0)
    rede = Condicional()
    treina_condicional(rede, imgs[treino], familia[treino],
                       beta=beta)
    rede.eval()
    with torch.no_grad():
        saida = rede.desenha(z.repeat(6, 1), todas)
        visto = juiz(saida).argmax(1)
    saida = saida.view(6, 500, -1)
    # quanto muda trocando a família, contra trocando a alma
    familias = (saida - saida.mean(0)).pow(2).mean()
    almas = (saida - saida.mean(1, keepdim=True)).pow(2).mean()
    certo = (visto == todas).float().view(6, 500).mean(1)
    print(f"{beta:4} {familias / almas:7.2f}  "
          + " ".join(f"{c:6.0%}" for c in certo))
with torch.no_grad():
    mu, _ = rede.codifica(imgs[:1], familia[:1])
    rosa = rede.desenha(mu.expand(6, 16), torch.arange(6))
oito = saida[:, :8].reshape(-1, 3, 32, 32)
grade(torch.cat([oito, imgs[:1], rosa, imgs[:1]]),
      "condicional.png", colunas=8)
