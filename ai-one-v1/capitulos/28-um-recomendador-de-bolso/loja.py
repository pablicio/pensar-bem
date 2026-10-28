import math
import random


def gerar_loja(semente, n_discos=120, n_clientes=200):
    # cada disco tem duas qualidades escondidas, de -1 a 1:
    # quanto dança e quanto é pernambucano; e uma fama.
    # Cada cliente tem um gosto para cada qualidade
    random.seed(semente)
    discos = []
    for _ in range(n_discos):
        danca = random.uniform(-1, 1)
        pe = random.uniform(-1, 1)
        fama = random.gauss(0, 0.8)
        discos.append((danca, pe, fama))
    compras = []
    for _ in range(n_clientes):
        g_danca = random.uniform(-1, 1)  # gosto por dança
        g_pe = random.uniform(-1, 1)     # gosto por Pernambuco
        pesos = [math.exp(3 * g_danca * d + 2 * g_pe * p + f)
                 for d, p, f in discos]
        quantas = random.randint(6, 16)
        cliente = []
        while len(cliente) < quantas:
            d = random.choices(range(n_discos), pesos)[0]
            if d not in cliente:
                cliente.append(d)
        compras.append(cliente)
    return discos, compras


def genero(disco):
    # o rótulo da prateleira, que o Beto daria olhando o disco
    danca, pe, _ = disco
    if danca > 0:
        return "frevo" if pe > 0 else "funk"
    return "viola" if pe > 0 else "jazz"
