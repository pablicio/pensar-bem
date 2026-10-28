import torch

from folha.conjunto import CLASSES, parte, tabela
from folha.siamesa import Projecao, perda_tripla

xt, rotulo = torch.load("caracteristicas.pt")["treino"]
verdade = torch.tensor([CLASSES.index(f["verdade"])
                        for f in tabela()
                        if parte(f["fazenda"]) == "treino"])
for nome, yt in (("rótulos do Dr. Edson", rotulo),
                 ("o que foi desenhado", verdade)):
    torch.manual_seed(0)
    projecao = Projecao()
    params = projecao.parameters()
    otimizador = torch.optim.Adam(params, lr=1e-3)
    sorteador = torch.Generator().manual_seed(1)
    for passo in range(1, 1001):
        # lote equilibrado: 20 fotos de cada uma das 6 classes
        lote = torch.cat([
            (yt == c).nonzero().flatten()[
                torch.randint((yt == c).sum(), (20,),
                              generator=sorteador)]
            for c in range(6)])
        otimizador.zero_grad()
        p = perda_tripla(projecao(xt[lote]), yt[lote])
        p.backward()
        otimizador.step()
    print(f"{nome:21} perda tripla no fim {p.item():.3f}")
    if yt is rotulo:                    # a que o projeto teria
        torch.save(projecao.state_dict(), "projecao.pt")
