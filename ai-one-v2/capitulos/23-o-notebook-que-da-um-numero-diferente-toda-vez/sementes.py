from roda_celulas import roda

ordem = [1, 2, 3, 4, 5, 6]
um = roda(ordem, semente=1)["credito"]
outro = roda(ordem, semente=2)["credito"]
diferentes = um[um != outro]
print(len(diferentes), "cooperados com crédito diferente")
print(f"maior diferença: R$ {abs(um - outro).max():.2f}")
print(f"soma: R$ {um.sum():,.2f} e R$ {outro.sum():,.2f}")
