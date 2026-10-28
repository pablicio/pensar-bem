from leitora.calibra import erro_de_calibracao, por_faixa
from leitora.carrega import leitora, probabilidades
from leitora.dados import MNIST, CaixasDoCartao

modelo = leitora()
valid = CaixasDoCartao("validacao")
conjuntos = [("MNIST, teste", MNIST("teste")),
             ("cartões, validação", valid)]
for nome, d in conjuntos:
    p = probabilidades(modelo, d.imagens)
    confianca, previsto = p.max(dim=1)
    acerto = (previsto == d.rotulos).float().mean()
    print(f"{nome:19} acerto {acerto:.2%}, confiança média"
          f" {confianca.mean():.2%}, ECE"
          f" {erro_de_calibracao(p, d.rotulos):.2%}")

print(f"\n{'faixa':>11} {'caixas':>7}"
      f" {'confiança':>10} {'acerto':>7}")
for a, b, k, conf, certo in por_faixa(p, d.rotulos):
    print(f"{a:5.1f}–{b:3.1f} {k:7} {conf:10.1%} {certo:7.1%}")
