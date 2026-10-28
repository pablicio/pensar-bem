import random

from sigmoide import sigmoide


def treinar_groove(r, k, eta, lam, epocas, semente, versao):
    # "escrita": pares não comprados, alvo 1 (o slide)
    # "indice": pares comprados, alvo 1 (índice trocado)
    # "completa": todos os pares, alvo r (entropia cruzada)
    random.seed(semente)
    n_c, n_d = len(r), len(r[0])
    p = [[random.gauss(0, 0.1) for _ in range(k)]
         for _ in range(n_c)]
    q = [[random.gauss(0, 0.1) for _ in range(k)]
         for _ in range(n_d)]
    for _ in range(epocas):
        gp = [[2 * lam * x for x in linha] for linha in p]
        gq = [[2 * lam * x for x in linha] for linha in q]
        for c in range(n_c):
            for d in range(n_d):
                if versao == "escrita" and r[c][d] == 1:
                    continue
                if versao == "indice" and r[c][d] == 0:
                    continue
                alvo = r[c][d] if versao == "completa" else 1
                z = sum(x * y for x, y in zip(p[c], q[d]))
                e = sigmoide(z) - alvo
                for f in range(k):
                    gp[c][f] += e * q[d][f]
                    gq[d][f] += e * p[c][f]
        for c in range(n_c):
            for f in range(k):
                p[c][f] -= eta * gp[c][f]
        for d in range(n_d):
            for f in range(k):
                q[d][f] -= eta * gq[d][f]
    return p, q
