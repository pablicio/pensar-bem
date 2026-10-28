from fatoracao import matriz, recomendar_fatores
from loja import gerar_loja, genero
from slide27 import treinar_groove

GENEROS = ["frevo", "funk", "viola", "jazz"]
discos, compras = gerar_loja(2027)
treino = [c[:-1] for c in compras]
r = matriz(treino, len(discos))
sem_fama = [0.0] * len(discos)
for versao in ["escrita", "completa"]:
    p, q = treinar_groove(r, k=3, eta=0.02, lam=0.01,
                          epocas=300, semente=2, versao=versao)
    recs = recomendar_fatores(1, treino[1], p, q, sem_fama)
    nomes = [genero(discos[d]) for d in recs]
    n = [nomes.count(g) for g in GENEROS]
    print(f"{versao:9} frevo {n[0]}, funk {n[1]}, "
          f"viola {n[2]}, jazz {n[3]}")
