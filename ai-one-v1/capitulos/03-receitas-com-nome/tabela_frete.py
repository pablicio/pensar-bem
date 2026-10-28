from frete import frete, peso_pacote

for n in range(1, 11):
    p = peso_pacote(n)
    print(f"{n:2d} discos  {p:5d} g  R$ {frete(p):6.2f}")
