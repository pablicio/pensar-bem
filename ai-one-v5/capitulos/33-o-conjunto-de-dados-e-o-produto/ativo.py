import matplotlib.pyplot as plt
import torch

from folha.emprestada import treina_cabeca

m = torch.load("caracteristicas.pt")
(xt, yt), (xv, yv) = m["treino"], m["validacao"]
INICIO, LOTE, ORCAMENTO = 50, 50, 500


def acerto(rotuladas):
    cabeca = treina_cabeca(xt[rotuladas], yt[rotuladas])
    with torch.no_grad():
        prevista = cabeca(xv).argmax(dim=1)
        confianca = cabeca(xt).softmax(dim=1).max(dim=1).values
    incerteza = 1 - confianca
    return (prevista == yv).float().mean().item(), incerteza


def rodada(estrategia, semente):
    """Uma curva, do sorteio inicial ao orçamento inteiro."""
    sorteador = torch.Generator().manual_seed(semente)
    ordem = torch.randperm(len(yt), generator=sorteador)
    rotuladas = ordem[:INICIO].tolist()
    curva = []
    while True:
        a, incerteza = acerto(rotuladas)
        curva.append(a)
        if len(rotuladas) >= ORCAMENTO:
            return curva
        livres = torch.ones(len(yt), dtype=torch.bool)
        livres[rotuladas] = False
        if estrategia == "ao acaso":
            candidatas = ordem[livres[ordem]]
        else:                          # as de menor confiança
            nota = incerteza.masked_fill(~livres, -1)
            candidatas = nota.argsort(descending=True)
        rotuladas += candidatas[:LOTE].tolist()


fotos = list(range(INICIO, ORCAMENTO + 1, LOTE))
fig, ax = plt.subplots(figsize=(6, 3.4))
marcas = "".join(f"{n:6}" for n in fotos[::3])
print("fotos rotuladas:  " + marcas)
for estrategia in ("ao acaso", "incerteza"):
    curvas = torch.tensor([rodada(estrategia, s)
                           for s in range(5)])
    media = curvas.mean(dim=0)
    print(f"{estrategia:16}  " + "".join(f"{a:6.1%}"
                                       for a in media[::3]))
    ax.plot(fotos, media, marker="o", label=estrategia)
todas = acerto(list(range(len(yt))))[0]
print(f"com as {len(yt)} fotos rotuladas: {todas:.1%}")
ax.axhline(todas, color="gray", ls="--",
           label="todas as fotos")
ax.set_xlabel("fotos rotuladas")
ax.set_ylabel("acerto na validação")
ax.legend()
fig.tight_layout()
fig.savefig("ativo.png", dpi=300)
