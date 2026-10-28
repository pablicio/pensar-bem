import random

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch import nn

from lupa.cabecas import VariasCabecas
from lupa.diario import atos, gabarito
from lupa.extrator import (PRAZO, VALOR, Vocabulario, limpa,
                           tokens)

CATEGORIAS = ["viaria", "edificacao", "servico", "compra",
              "outro"]
REGIOES = ["cabeçalho", "objeto", "valor", "prazo", "resto"]


def exemplos():
    """(tokens, prazo, categoria, nº de dígitos e primeiro
    dígito do valor, em reais) de cada extrato."""
    verdade, lista = gabarito(), []
    for a in atos():
        if a["tipo"] != "extrato":
            continue
        t = limpa(a["texto"])
        reais = [c for c in VALOR.search(t).group(1)
                 if c.isdigit()][:-2]       # sem os centavos
        cat = verdade[a["id"]]["categoria"]
        prazo = PRAZO.search(t).group(1)
        lista.append((tokens(t)[:256], prazo,
                      CATEGORIAS.index(cat), len(reais),
                      int(reais[0])))
    return lista


class Leitor(nn.Module):
    """Uma consulta aprendida lê o extrato com h cabeças, e
    quatro camadas lineares respondem as quatro perguntas."""

    def __init__(self, n_voc, classes, d=64, h=4):
        super().__init__()
        self.emb = nn.Embedding(n_voc, d, padding_idx=0)
        self.pos = nn.Embedding(256, d)
        inicial = 0.1 * torch.randn(1, 1, d)
        self.consulta = nn.Parameter(inicial)
        self.atencao = VariasCabecas(d, h)
        self.saidas = nn.ModuleList(nn.Linear(d, c)
                                    for c in classes)

    def forward(self, x):
        T = x.shape[1]
        e = self.emb(x) + self.pos(torch.arange(T))
        q = self.consulta.expand(x.shape[0], 1, -1)
        pad = (x == 0)[:, None, None, :]
        o = self.atencao(q, e, pad)[:, 0]
        return [saida(o) for saida in self.saidas]


def regioes(e):
    o = e.index("objeto")
    v = e.index("valor", o)
    p = e.index("prazo", v)
    a = e.index("assinatura", p)
    return [range(0, o), range(o, v), range(v, p),
            range(p, a + 2), range(a + 2, len(e))]


random.seed(0)
dados = exemplos()
random.shuffle(dados)
teste, treino = dados[:400], dados[400:]
voc = Vocabulario([d[0] for d in treino])
prazos = sorted({d[1] for d in dados})
tamanhos = sorted({d[3] for d in dados})


def lote(ds):
    x = torch.zeros(len(ds), max(len(d[0]) for d in ds),
                    dtype=torch.long)
    for i, d in enumerate(ds):
        x[i, :len(d[0])] = torch.tensor(voc.codifica(d[0]))
    ys = [[prazos.index(d[1]) for d in ds],
          [d[2] for d in ds],
          [tamanhos.index(d[3]) for d in ds],
          [d[4] for d in ds]]
    return x, [torch.tensor(y) for y in ys]


print("cabeças  parâmetros  prazo  categoria  dígitos"
      "  1º dígito")
massas = {}
for h in [1, 4]:
    random.seed(0)
    torch.manual_seed(0)
    m = Leitor(len(voc), [len(prazos), 5, len(tamanhos), 10],
               h=h)
    opt = torch.optim.Adam(m.parameters(), 3e-3)
    for epoca in range(20):
        random.shuffle(treino)
        for k in range(0, len(treino), 32):
            x, ys = lote(treino[k:k + 32])
            perda = sum(F.cross_entropy(o, y)
                        for o, y in zip(m(x), ys))
            opt.zero_grad()
            perda.backward()
            opt.step()
    with torch.no_grad():
        x, ys = lote(teste)
        acertos = [(o.argmax(-1) == y).float().mean().item()
                   for o, y in zip(m(x), ys)]
        P = m.atencao.pesos[:, :, 0]          # (400, h, T)
    n = sum(p.numel() for p in m.parameters())
    larguras = [7, 11, 9, 11]
    print(f"{h:7} {n:11}" + "".join(
        f"{a:{w}.0%}" for a, w in zip(acertos, larguras)))
    massa = torch.zeros(h, 5)
    for i, d in enumerate(teste):
        for r, pos in enumerate(regioes(d[0])):
            soma = P[i, :, list(pos)].sum(-1)
            massa[:, r] += soma / len(teste)
    massas[h] = massa

print("\nonde cada cabeça põe o peso:")
print(" " * 12 + "".join(f"{r:>10}" for r in REGIOES))
linhas = [("1 cabeça", massas[1][0])] + [
    (f"cabeça {i + 1}", massas[4][i]) for i in range(4)]
for nome, massa in linhas:
    print(f"{nome:12}" + "".join(f"{v:10.2f}" for v in massa))

fig, eixo = plt.subplots(figsize=(6, 3))
matriz = torch.stack([m for _, m in linhas]).numpy()
eixo.imshow(matriz, cmap="Greys", vmin=0, vmax=1)
for i in range(5):
    for j in range(5):
        cor = "white" if matriz[i, j] > 0.5 else "black"
        eixo.text(j, i, f"{matriz[i, j]:.2f}", ha="center",
                  va="center", color=cor, fontsize=8)
eixo.set_xticks(range(5), REGIOES)
eixo.set_yticks(range(5), [n for n, _ in linhas])
fig.tight_layout()
fig.savefig("cabecas.png", dpi=300)
