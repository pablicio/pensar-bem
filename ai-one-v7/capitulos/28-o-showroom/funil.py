import numpy as np
import torch

from lauber.acervo import carrega, grade, partes
from lauber.classificador import Classificador, treina
from lauber.dcgan import CODIGO, desenha
from lauber.emenda import GeradorCircular, costura
from lauber.serigrafia import delta_e, reduz
from lauber.vitrine import parecenca
from lauber.vizinhos import normaliza, vizinho

imgs, info = carrega()
familia = torch.tensor(info["familia"])
treino, _, teste = partes(len(imgs))
torch.manual_seed(0)
juiz = Classificador()          # o juiz do capítulo 1
treina(juiz, imgs[treino], familia[treino])
gerador = GeradorCircular()     # o do capítulo 25
gerador.load_state_dict(torch.load("emenda.pt"))

torch.manual_seed(2)
x = desenha(gerador, torch.randn(8000, CODIGO))
with torch.no_grad():
    chance = juiz(x).softmax(1)
print(f"8000 candidatas, parecença {parecenca(x[:500]):.2f}")
pedidas = {"florais": 3, "listras": 0}
vivas = {}
for nome, k in pedidas.items():
    vivas[nome] = torch.arange(8000)[chance[:, k] > 0.9]


def etapa(titulo, passa):
    """passa(indices) diz, para cada índice, se ele fica."""
    for nome in vivas:
        v = vivas[nome]
        vivas[nome] = v[torch.as_tensor(passa(v))]
    print(f"{titulo:35} {len(vivas['florais']):7d}"
          f" {len(vivas['listras']):8d}")


def emenda(v):
    return [costura(x[i:i + 1]) < 1.1 for i in v.tolist()]


def nao_copia(v):
    return vizinho(x[v], imgs[treino], espelho=True)[1] < 0.99


def seis_cores(v):
    fica = []
    for img in x[v].permute(0, 2, 3, 1).numpy().astype(float):
        rotulos, paleta = reduz(img, 6)
        fica.append(delta_e(img, paleta[rotulos]) < 20)
    return fica


print("etapa                               florais  listras")
etapa("o juiz tem mais de 90% de certeza",
      lambda v: [True] * len(v))
etapa("emenda (costura < 1,1)", emenda)
etapa("não é cópia (correlação < 0,99)", nao_copia)
etapa("seis cores com ΔE < 20", seis_cores)

# as mais claras para o juiz, sem duas quase iguais
escolha = []
for nome, quantas in (("florais", 12), ("listras", 8)):
    k = pedidas[nome]
    ordem = vivas[nome][chance[vivas[nome], k].argsort(
        descending=True)]
    novas = []
    for i in ordem.tolist():
        a = normaliza(x[i:i + 1])
        if all((a @ normaliza(x[j:j + 1]).T).item() < 0.7
               for j in novas):
            novas.append(i)
        if len(novas) == quantas:
            break
    print(f"{nome}: {len(novas)} escolhidas, sem quase iguais")
    escolha += novas
grade(x[escolha], "vitrine.png", colunas=10)
torch.save(x[escolha], "vitrine.pt")    # para o capítulo 29
