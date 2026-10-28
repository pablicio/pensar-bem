from frete import frete


def peso_compacto(n):
    return 150 + 70 * n


for n in range(1, 6):
    p = peso_compacto(n)
    print(f"{n} compactos  {p:4d} g  R$ {frete(p):5.2f}")
