from matriz import matriz_vezes_vetor, multiplicar, transposta
from operacoes import escalar, media, soma
from potencia import iteracao_potencia

pontos = []
with open("nuvem.csv", encoding="utf-8") as arquivo:
    arquivo.readline()
    for linha in arquivo:
        campos = linha.strip().split(",")
        pontos.append([float(campos[1]), float(campos[2])])

centro = media(pontos)
X = [soma(p, escalar(-1, centro)) for p in pontos]
M = multiplicar(transposta(X), X)
d, lam = iteracao_potencia(M)
outra = [-d[1], d[0]]  # perpendicular à primeira
Mv = matriz_vezes_vetor(M, outra)
print("segunda direção:", [round(x, 3) for x in outra])
print("M v / v:", [round(a / b, 4) for a, b in zip(Mv, outra)])
print("autovalores:", round(lam, 4),
      round(Mv[0] / outra[0], 4))
