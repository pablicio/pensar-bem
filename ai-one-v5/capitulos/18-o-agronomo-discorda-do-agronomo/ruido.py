import torch

from folha.conjunto import CLASSES, parte, tabela
from folha.emprestada import treina_cabeca

matrizes = torch.load("caracteristicas.pt")
xt, _ = matrizes["treino"]
xv, _ = matrizes["validacao"]
vt, vv = (torch.tensor([CLASSES.index(f["verdade"])
                        for f in tabela()
                        if parte(f["fazenda"]) == q])
          for q in ("treino", "validacao"))
SOL, FERRUGEM = CLASSES.index("sol"), CLASSES.index("ferrugem")
sorteador = torch.Generator().manual_seed(0)


def ao_acaso(taxa):
    """Troca uma fração dos rótulos por uma classe qualquer."""
    y = vt.clone()
    troca = torch.rand(len(y), generator=sorteador) < taxa
    y[troca] = torch.randint(0, 6, (int(troca.sum()),),
                             generator=sorteador)
    return y


def sol_vira_ferrugem(taxa):
    """Rotula como ferrugem uma fração das folhas de sol."""
    y = vt.clone()
    sois = (vt == SOL).nonzero().flatten()
    ordem = torch.randperm(len(sois), generator=sorteador)
    y[sois[ordem[:int(taxa * len(sois))]]] = FERRUGEM
    return y


print("ruído no treino          acerto  sol  sol → ferrugem")
casos = [("nenhum", vt), ("20% ao acaso", ao_acaso(0.2)),
         ("40% ao acaso", ao_acaso(0.4)),
         ("40% do sol → ferrugem", sol_vira_ferrugem(0.4))]
for nome, y in casos:
    prevista = treina_cabeca(xt, y)(xv).argmax(dim=1)
    sol = prevista[vv == SOL]
    print(f"{nome:23} {(prevista == vv).float().mean():6.1%}"
          f" {(sol == SOL).float().mean():4.0%}"
          f" {(sol == FERRUGEM).sum():6} de {len(sol)}")
