import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from lupa.bloco import Pilha
from lupa.diario import atos
from lupa.extrator import limpa

torch.manual_seed(0)
texto = "\n".join(limpa(a["texto"]) for a in atos()[:3000])
letras = sorted(set(texto))
dados = torch.tensor([letras.index(c) for c in texto])
V, T, L = len(letras), 64, 12
print(V, "caracteres diferentes,", len(dados), "no texto")


def lote():
    i = torch.randint(0, len(dados) - T - 1, (32,))
    x = torch.stack([dados[j:j + T] for j in i])
    y = torch.stack([dados[j + 1:j + T + 1] for j in i])
    return x, y


# 1. o tamanho do fluxo residual, bloco a bloco, ao nascer
x, y = lote()
print("\ndesvio do fluxo nos blocos 1, 3, 6, 9 e 12:")
for escala in [False, True]:
    torch.manual_seed(0)
    fluxo = []
    Pilha(V, L, T=T, escala=escala)(x, fluxo)
    nome = "inicialização do GPT-2" if escala else "padrão"
    escolhidos = [fluxo[i] for i in (0, 2, 5, 8, 11)]
    print(f"  {nome:23}",
          " ".join(f"{v:.2f}" for v in escolhidos))

# 2. pré e pós-normalização, sem aquecimento
curvas = {}
for pre in [True, False]:
    torch.manual_seed(0)
    m = Pilha(V, L, T=T, pre=pre)
    opt = torch.optim.Adam(m.parameters(), lr=3e-3)
    perdas = []
    for passo in range(150):
        x, y = lote()
        logits = m(x).flatten(0, 1)
        perda = F.cross_entropy(logits, y.flatten())
        opt.zero_grad()
        perda.backward()
        opt.step()
        perdas.append(perda.item())
    nome = "pré" if pre else "pós"
    curvas[nome] = perdas
    medias = [sum(perdas[i:i + 50]) / 50 for i in (0, 50, 100)]
    print(f"{nome}: perda nos passos 1-50, 51-100,"
          " 101-150:", " ".join(f"{p:.2f}" for p in medias))

fig, eixo = plt.subplots(figsize=(6, 3))
for nome, perdas in curvas.items():
    eixo.plot(perdas, label=f"{nome}-normalização")
eixo.set_xlabel("passo")
eixo.set_ylabel("perda")
eixo.legend()
fig.tight_layout()
fig.savefig("pre_pos.png", dpi=300)
