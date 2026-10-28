import time

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from lupa.tradutor import Tradutor, pares

torch.manual_seed(0)
treino, teste = pares(8000, semente=1), pares(1000, semente=2)
palavras = sorted({p for e, _ in treino for p in e})
ent = {p: i + 1 for i, p in enumerate(palavras)}   # 0 = pad
saida = ["<ini>"] + list("0123456789-")
sai = {c: i for i, c in enumerate(saida)}
print(len(palavras), "palavras de entrada; exemplo:")
print(" ", " ".join(treino[0][0]), "->", "".join(treino[0][1]))


def lote(ps):
    T = max(len(e) for e, _ in ps)
    x = torch.zeros(len(ps), T, dtype=torch.long)
    for i, (e, _) in enumerate(ps):
        x[i, :len(e)] = torch.tensor([ent[p] for p in e])
    y = torch.tensor([[sai[c] for c in s] for _, s in ps])
    ini = torch.zeros(len(ps), 1, dtype=torch.long)
    y_in = torch.cat([ini, y[:, :-1]], dim=1)   # <ini> + y
    return x, y_in, y


modelo = Tradutor(len(ent) + 1, len(saida))
n = sum(p.numel() for p in modelo.parameters())
print(n, "parâmetros")
opt = torch.optim.Adam(modelo.parameters(), lr=1e-3)
inicio = time.time()
for epoca in range(1, 9):
    for k in range(0, len(treino), 64):
        x, y_in, y = lote(treino[k:k + 64])
        perda = F.cross_entropy(modelo(x, y_in).flatten(0, 1),
                                y.flatten())
        opt.zero_grad()
        perda.backward()
        opt.step()
    print(f"época {epoca}  perda {perda.item():.4f}")
print(f"treino: {time.time() - inicio:.0f} s")


@torch.no_grad()
def traduz(x):
    """Gulosa: um caractere de cada vez, a partir de <ini>."""
    y = torch.zeros(len(x), 1, dtype=torch.long)
    for _ in range(10):
        proximo = modelo(x, y)[:, -1].argmax(-1, keepdim=True)
        y = torch.cat([y, proximo], dim=1)
    return y[:, 1:]


x, _, y = lote(teste)
certas = (traduz(x) == y).all(dim=1).float().mean()
print(f"datas do teste traduzidas sem erro: {certas:.1%}")

# o mapa da atenção cruzada da última camada, para um exemplo
e, s = teste[3]
x, y_in, _ = lote([(e, s)])
with torch.no_grad():
    modelo(x, y_in)
pesos = modelo.dec[-1].cruzada.pesos[0].mean(dim=0)  # média
print(" ".join(e), "->", "".join(s))
fig, eixo = plt.subplots(figsize=(6, 3.5))
eixo.imshow(pesos, cmap="Greys", aspect="auto")
eixo.set_xticks(range(len(e)), e, rotation=60, fontsize=8)
eixo.set_yticks(range(len(s)), s)
eixo.set_xlabel("data por extenso (codificador)")
eixo.set_ylabel("o que o decodificador escreve")
fig.tight_layout()
fig.savefig("datas.png", dpi=300)
