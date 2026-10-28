import matplotlib.pyplot as plt
import torch

from folha.conjunto import parte, tabela
from folha.emprestada import treina_cabeca

matrizes = torch.load("caracteristicas.pt")
xt, yt = matrizes["treino"]
xv, yv = matrizes["validacao"]

# ações: 0 não tratar, 1 contra ferrugem, 2 cercosporiose,
# 3 bicho-mineiro, 4 phoma; sadia e sol pedem a ação 0
ACAO = torch.tensor([0, 1, 2, 3, 4, 0])
APLICAR = torch.tensor([0, 380, 380, 380, 380.0])   # R$/ha
PERDA = torch.tensor([0, 2000, 1200, 900, 1200, 0.0])
errada = ACAO[:, None] != torch.arange(5)[None, :]
custo = APLICAR[None, :] + PERDA[:, None] * errada  # 6 × 5
C = custo - custo.min(dim=1, keepdim=True).values  # o perdido
print("custo de cada erro (R$/ha), classe × ação:")
print(C.int())


def fora_da_dobra():
    """Probabilidades do treino, cada fazenda julgada por uma
    cabeça que não a viu (como no capítulo 18)."""
    linhas = [f for f in tabela()
              if parte(f["fazenda"]) == "treino"]
    fazendas = sorted({f["fazenda"] for f in linhas})
    dobra = torch.tensor([fazendas.index(f["fazenda"]) % 5
                          for f in linhas])
    P = torch.zeros(len(yt), 6)
    for k in range(5):
        cabeca = treina_cabeca(xt[dobra != k], yt[dobra != k])
        with torch.no_grad():
            P[dobra == k] = cabeca(xt[dobra == k]).softmax(1)
    return P


def maior(P):
    return ACAO[P.argmax(dim=1)]


def risco(P):
    return (P @ C).argmin(dim=1)        # N × 6 · 6 × 5


def limiar(t):
    def regra(P):
        acao = maior(P)
        acao[P[:, 1] >= t] = 1          # ferrugem desde t
        return acao
    return regra


def balanco(P, y, regra):
    acao = regra(P)
    perdidas = ((y == 1) & (acao != 1)).sum()
    a_mais = ((y != 1) & (acao == 1)).sum()
    return C[y, acao].sum().item(), perdidas, a_mais


Pt = fora_da_dobra()
cabeca = treina_cabeca(xt, yt)
with torch.no_grad():
    Pv = cabeca(xv).softmax(dim=1)
REGRAS = [("maior prob.", maior), ("risco mínimo", risco),
          ("limiar 0,2", limiar(0.2))]
for nome_parte, P, y in [("treino, fora da dobra", Pt, yt),
                         ("validação", Pv, yv)]:
    print(f"\n{nome_parte}")
    print("  regra            custo  ferrugem perdida  a mais")
    for nome, regra in REGRAS:
        custo_total, perdidas, a_mais = balanco(P, y, regra)
        print(f"  {nome:13} {custo_total:7,.0f} {perdidas:17}"
              f" {a_mais:7}")

limiares = [i / 100 for i in range(2, 100, 2)]
custos = [balanco(Pt, yt, limiar(t))[0] for t in limiares]
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.plot(limiares, custos)
ax.axhline(balanco(Pt, yt, maior)[0], color="gray", ls="--",
           label="maior probabilidade")
ax.set_xlabel("limiar de probabilidade para tratar ferrugem")
ax.set_ylabel("custo no treino (R$)")
ax.legend()
fig.tight_layout()
fig.savefig("limiar.png", dpi=300)
