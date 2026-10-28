from clientes import ler_clientes
from matriz import matriz_vezes_vetor, transposta

nomes, C = ler_clientes("clientes.csv")
estilos = ["frevo", "choro", "jazz", "rock", "forro", "mpb"]

por_cliente = matriz_vezes_vetor(C, [1, 1, 1, 1, 1, 1])
por_estilo = matriz_vezes_vetor(transposta(C),
                                [1, 1, 1, 1, 1, 1])
for nome, total in zip(nomes, por_cliente):
    print(f"{nome:13s} {total:3d} discos")
for estilo, total in zip(estilos, por_estilo):
    print(f"{estilo:6s} {total:3d} discos")
