from demanda import demanda


def lucro_limitado(preco):
    vendidas = min(demanda(preco), 100)
    return (preco - 38.00) * vendidas


precos = [40 + 0.1 * k for k in range(1101)]
lucros = [lucro_limitado(p) for p in precos]
lucro_max, preco_max = max(zip(lucros, precos))
print(f"R$ {preco_max:.2f}, lucro de R$ {lucro_max:.2f}")
print(f"demanda nesse preço: {demanda(preco_max):.1f} cópias")
