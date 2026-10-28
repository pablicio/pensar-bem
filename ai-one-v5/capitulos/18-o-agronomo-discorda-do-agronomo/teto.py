import torch

from folha.conjunto import CLASSES, parte, tabela
from folha.emprestada import treina_cabeca

matrizes = torch.load("caracteristicas.pt")
xt, yt = matrizes["treino"]          # rótulos do Dr. Edson
xv, yv = matrizes["validacao"]


def verdade(qual):
    """O que o gerador desenhou, na ordem da Folhas."""
    return torch.tensor([CLASSES.index(f["verdade"])
                         for f in tabela()
                         if parte(f["fazenda"]) == qual])


vt, vv = verdade("treino"), verdade("validacao")
print(f"rótulos errados: treino {(yt != vt).sum()}"
      f" de {len(yt)}, validação {(yv != vv).sum()}"
      f" de {len(yv)}")
print("treino com           medido pelo Edson  pela verdade")
for nome, alvo in [("rótulos do Edson", yt),
                   ("o que foi desenhado", vt)]:
    prevista = treina_cabeca(xt, alvo)(xv).argmax(dim=1)
    contra_edson = (prevista == yv).float().mean()
    contra_verdade = (prevista == vv).float().mean()
    print(f"{nome:20} {contra_edson:17.1%}"
          f" {contra_verdade:13.1%}")
