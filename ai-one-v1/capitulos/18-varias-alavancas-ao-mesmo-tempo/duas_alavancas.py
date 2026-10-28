import math

CUSTO = 38.00


def lucro(preco, anuncio):
    # anúncio em R$/mês; o efeito cresce cada vez mais devagar
    alcance = 1 + 0.6 * (1 - math.exp(-anuncio / 400))
    vendas = 500 * math.exp(-0.02 * preco) * alcance
    return (preco - CUSTO) * vendas - anuncio


def gradiente(f, x, y, h=1e-4):
    dx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    dy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    return dx, dy
