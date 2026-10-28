from fatoracao import matriz, recomendar_fatores
from loja import gerar_loja
from slide27 import treinar_groove

discos, compras = gerar_loja(2027)
treino = [c[:-1] for c in compras]
r = matriz(treino, len(discos))
sem_fama = [0.0] * len(discos)
for versao in ["escrita", "indice", "completa"]:
    p, q = treinar_groove(r, k=3, eta=0.02, lam=0.01,
                          epocas=300, semente=2, versao=versao)
    acertos = 0
    for c, todas in enumerate(compras):
        recs = recomendar_fatores(c, treino[c], p, q, sem_fama)
        if todas[-1] in recs:
            acertos += 1
    print(f"{versao:9} taxa de acerto em 10: "
          f"{acertos / len(compras):.3f}")
