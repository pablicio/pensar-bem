import math

from clientes import ler_clientes
from matriz import multiplicar, transposta

nomes, R = ler_clientes("notas.csv")

# dois números por disco: de dançar e de ouvir sentado
# frevo, forró, rock, choro, bossa, jazz
discos = [[1.0, 0.1], [0.9, 0.3], [0.8, 0.0],
          [0.2, 1.0], [0.1, 0.9], [0.0, 1.0]]
# dois números por cliente: quanto gosta de cada tipo, de 0 a 5
gostos = [[4, 3], [4, 4], [5, 0], [1, 5],
          [2, 2], [4, 1], [0, 4], [3, 5]]


def erro_medio(A, B):
    total = 0
    n = 0
    for linha_a, linha_b in zip(A, B):
        for a, b in zip(linha_a, linha_b):
            total += (a - b) ** 2
            n += 1
    return math.sqrt(total / n)


R_hat = multiplicar(gostos, transposta(discos))
print("Marina, nota real:    ", R[3])
print("Marina, reconstruída: ",
      [round(x, 1) for x in R_hat[3]])
print(f"erro médio com 2 fatores: {erro_medio(R, R_hat):.2f}")

so_danca_gostos = [[g[0]] for g in gostos]
so_danca_discos = [[d[0]] for d in discos]
R_um = multiplicar(so_danca_gostos,
                   transposta(so_danca_discos))
print("Marina, só dança:     ", [round(x, 1) for x in R_um[3]])
print(f"erro médio com 1 fator:  {erro_medio(R, R_um):.2f}")
