from loja import gerar_loja, genero
from recomenda import recomendar, similaridades

discos, compras = gerar_loja(2027)
treino = [c[:-1] for c in compras]
sim = similaridades(treino, len(discos))


def por_genero(lista):
    nomes = [genero(discos[d]) for d in lista]
    generos = ["frevo", "funk", "viola", "jazz"]
    return [(g, nomes.count(g)) for g in generos]


c = treino[1]
print("comprou:    ", por_genero(c))
print("recomendado:", por_genero(recomendar(c, sim)))
print("escondida:  ", genero(discos[compras[1][-1]]))
