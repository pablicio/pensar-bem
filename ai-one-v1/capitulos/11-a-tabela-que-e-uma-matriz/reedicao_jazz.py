from clientes import ler_clientes
from matriz import matriz_vezes_vetor

nomes, C = ler_clientes("clientes.csv")
afinidade = matriz_vezes_vetor(C, [0, 0.2, 0.8, 0, 0, 0])
for valor, nome in sorted(zip(afinidade, nomes), reverse=True):
    print(f"{nome:13s} {valor:5.1f}")
