clientes = 21_000
discos = 38_000
celulas = clientes * discos
compras = 120_000
parametros = 1_200_000_000            # o número do slide 11
print(f"células da matriz: {celulas:,}")
print(f"compras (uns):     {compras:,}")
print(f"fração preenchida: {compras / celulas:.5%}")
print(f"parâmetros por compra: {parametros / compras:,.0f}")
