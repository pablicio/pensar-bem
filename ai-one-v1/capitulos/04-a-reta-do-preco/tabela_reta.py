from reta import preco_justo

for nota in range(1, 11):
    print(f"nota {nota:2d}  R$ {preco_justo(nota):7.2f}")
