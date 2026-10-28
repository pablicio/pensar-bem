import random


def prever(pc, qd, bd):
    # o modelo: produto escalar mais a fama do disco
    return sum(x * y for x, y in zip(pc, qd)) + bd


def matriz(compras, n_discos):
    # uma linha por cliente: 1 se comprou o disco, 0 se não
    r = [[0] * n_discos for _ in compras]
    for c, discos in enumerate(compras):
        for d in discos:
            r[c][d] = 1
    return r


def treinar(r, k, eta, lam, epocas, semente, escala=0.1):
    # aprende p (clientes), q (discos) e b (fama) por descida
    random.seed(semente)
    n_c, n_d = len(r), len(r[0])
    p = [[random.gauss(0, escala) for _ in range(k)]
         for _ in range(n_c)]
    q = [[random.gauss(0, escala) for _ in range(k)]
         for _ in range(n_d)]
    b = [0.0] * n_d
    historico = []
    for _ in range(epocas):
        gp = [[2 * lam * x for x in linha] for linha in p]
        gq = [[2 * lam * x for x in linha] for linha in q]
        gb = [0.0] * n_d
        perda = 0
        for c in range(n_c):
            for d in range(n_d):
                e = prever(p[c], q[d], b[d]) - r[c][d]
                perda += e * e
                gb[d] += 2 * e
                for f in range(k):
                    gp[c][f] += 2 * e * q[d][f]
                    gq[d][f] += 2 * e * p[c][f]
        for c in range(n_c):
            for f in range(k):
                p[c][f] -= eta * gp[c][f]
        for d in range(n_d):
            for f in range(k):
                q[d][f] -= eta * gq[d][f]
            b[d] -= eta * gb[d]
        historico.append(perda)
    return p, q, b, historico


def recomendar_fatores(c, comprados, p, q, b, quantos=10):
    # a nota de cada disco não comprado é o modelo inteiro
    notas = []
    for d in range(len(q)):
        if d not in comprados:
            nota = prever(p[c], q[d], b[d])
            notas.append((nota, d))
    notas = sorted(notas, reverse=True)
    return [d for _, d in notas[:quantos]]
