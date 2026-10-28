from frete import frete, peso_pacote

for n in range(10, 16):
    p = peso_pacote(n)
    print(n, p, frete(p))
