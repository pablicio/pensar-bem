from clientes import ler_clientes
from matriz import matriz_vezes_vetor
from operacoes import escalar

nomes, C = ler_clientes("clientes.csv")
P = []
for linha in C:
    P.append(escalar(1 / sum(linha), linha))
afinidade = matriz_vezes_vetor(P, [0.7, 0, 0, 0, 0.3, 0])
for valor, nome in sorted(zip(afinidade, nomes), reverse=True):
    print(f"{nome:13s} {valor:.3f}")
