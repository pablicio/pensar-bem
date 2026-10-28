import torch

from folha.conjunto import CLASSES, parte, tabela
from folha.emprestada import treina_cabeca

matrizes = torch.load("caracteristicas.pt")
xt, yt = matrizes["treino"]
xv, yv = matrizes["validacao"]
linhas = {q: [f for f in tabela() if parte(f["fazenda"]) == q]
          for q in ("treino", "validacao")}
vt, vv = (torch.tensor([CLASSES.index(f["verdade"])
                        for f in ls])
          for ls in linhas.values())


@torch.no_grad()
def chance_do_rotulo(cabeca, x, y):
    """A probabilidade que a cabeça dá ao rótulo anotado."""
    p = torch.softmax(cabeca(x), dim=1)
    return p[torch.arange(len(y)), y]


# treino: cada fazenda é julgada por uma cabeça que não a viu
fazendas = sorted({f["fazenda"] for f in linhas["treino"]})
dobra = torch.tensor([fazendas.index(f["fazenda"]) % 5
                      for f in linhas["treino"]])
chance = torch.zeros(len(yt))
for k in range(5):
    fora, dentro = dobra != k, dobra == k
    cabeca = treina_cabeca(xt[fora], yt[fora])
    chance[dentro] = chance_do_rotulo(cabeca, xt[dentro],
                                      yt[dentro])
errados = yt != vt
ordem = chance.argsort()        # as mais suspeitas primeiro
print(f"treino: {errados.sum()} rótulos errados em {len(yt)}")
for k in (25, 50, 100):
    print(f"  revendo as {k:3} mais suspeitas, acham-se"
          f" {errados[ordem[:k]].sum():2} erros")

cabeca = treina_cabeca(xt, yt)
chance = chance_do_rotulo(cabeca, xv, yv)
errados = yv != vv
ordem = chance.argsort()
print(f"validação: {errados.sum()} rótulos errados"
      f" em {len(yv)}")
for k in (10, 30):
    print(f"  revendo as {k:3} mais suspeitas, acham-se"
          f" {errados[ordem[:k]].sum():2} erros")
