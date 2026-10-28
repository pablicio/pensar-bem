from demanda import demanda


def lucro(preco):
    return (preco - 45.00) * demanda(preco)


precos = [40 + 0.1 * k for k in range(1101)]
lucros = [lucro(p) for p in precos]
lucro_max, preco_max = max(zip(lucros, precos))
print(f"R$ {preco_max:.2f}, lucro de R$ {lucro_max:.2f}")
