from clientes import ler_clientes
from matriz import forma, matriz_vezes_vetor

nomes, C = ler_clientes("clientes.csv")
print("forma de C:", forma(C))

# a reedição: 70% frevo, 30% forró, nos seis estilos da tabela
g = [0.7, 0, 0, 0, 0.3, 0]
afinidade = matriz_vezes_vetor(C, g)

pares = sorted(zip(afinidade, nomes), reverse=True)
for valor, nome in pares:
    print(f"{nome:13s} {valor:5.1f}")
