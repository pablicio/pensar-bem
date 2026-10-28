from clientes import ler_clientes
from fatores import erro_medio
from matriz import multiplicar, transposta

nomes, R = ler_clientes("notas.csv")
medias = [[sum(linha) / len(linha)] for linha in R]
uns = [[1] for _ in range(6)]
R_media = multiplicar(medias, transposta(uns))
e = erro_medio(R, R_media)
print(f"erro médio, só a média de cada cliente: {e:.2f}")
