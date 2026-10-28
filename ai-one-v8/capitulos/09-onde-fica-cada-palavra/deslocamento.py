import math

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch import nn

from lupa.posicao import rope, senoidal

# a tarefa: repetir o token de ATRAS posições antes
V, D, ATRAS = 20, 32, 3


class Repetidor(nn.Module):
    """Uma cabeça de atenção causal e uma camada de saída."""

    def __init__(self, posicao):
        super().__init__()
        self.posicao = posicao
        self.emb = nn.Embedding(V, D)
        self.pos = nn.Embedding(256, D)      # para a aprendida
        self.W_q = nn.Linear(D, D, bias=False)
        self.W_k = nn.Linear(D, D, bias=False)
        self.W_v = nn.Linear(D, D, bias=False)
        self.saida = nn.Linear(D, V)

    def forward(self, x):
        T = x.shape[1]
        e = self.emb(x)
        v = self.W_v(e)
        if self.posicao == "aprendida":
            e = e + self.pos(torch.arange(T))
        elif self.posicao == "senoidal":
            e = e + senoidal(T, D)
        q, k = self.W_q(e), self.W_k(e)
        if self.posicao == "rope":
            q, k = rope(q), rope(k)
        notas = q @ k.transpose(-2, -1) / math.sqrt(D)
        futuro = torch.ones(T, T, dtype=torch.bool).triu(1)
        notas = notas.masked_fill(futuro, float("-inf"))
        return self.saida(notas.softmax(dim=-1) @ v)


@torch.no_grad()
def acerto_por_posicao(m, T):
    x = torch.randint(0, V, (512, T))
    certo = m(x).argmax(-1)[:, ATRAS:] == x[:, :-ATRAS]
    return certo.float().mean(dim=0)   # taxa por posição


print("posição     treino (64)   texto de 128")
curvas = {}
for posicao in ["nenhuma", "aprendida", "senoidal", "rope"]:
    torch.manual_seed(0)
    m = Repetidor(posicao)
    opt = torch.optim.Adam(m.parameters(), 3e-3)
    for passo in range(1500):
        x = torch.randint(0, V, (64, 64))   # textos de 64
        logits = m(x)[:, ATRAS:]
        perda = F.cross_entropy(logits.reshape(-1, V),
                                x[:, :-ATRAS].reshape(-1))
        opt.zero_grad()
        perda.backward()
        opt.step()
    curvas[posicao] = acerto_por_posicao(m, 128)
    no_treino = acerto_por_posicao(m, 64).mean()
    longo = curvas[posicao].mean()
    print(f"{posicao:11} {no_treino:9.1%} {longo:14.1%}")

fig, eixo = plt.subplots(figsize=(6, 3))
for posicao, curva in curvas.items():
    eixo.plot(range(ATRAS, 128), curva.numpy(), label=posicao)
eixo.axvline(64, color="gray", linestyle=":")
eixo.set_xlabel("posição no texto de 128 tokens")
eixo.set_ylabel("acerto")
eixo.legend()
fig.tight_layout()
fig.savefig("extrapolacao.png", dpi=300)
