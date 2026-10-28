import math


def peso_pacote(n):
    # caixa de 200 g, mais 230 g por disco (capa e plástico)
    return 200 + 230 * n


def frete(peso):
    if peso <= 300:
        return 18.00
    elif peso <= 1000:
        return 24.50
    elif peso <= 2000:
        return 31.00
    else:
        quilos_extras = math.ceil((peso - 2000) / 1000)
        return 31.00 + 6.50 * quilos_extras
