def br(valor, casas=2):
    """1234.5 -> '1.234,50'"""
    texto = f"{valor:,.{casas}f}"
    return texto.translate(str.maketrans(",.", ".,"))


assert br(1652.9, 1) == "1.652,9"
assert br(0.5) == "0,50"
assert br(1234567.891) == "1.234.567,89"
print(br(126809.824, 3))
