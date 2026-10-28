def registrar(**campos):
    for chave, valor in campos.items():
        print(f"{chave}: {valor}")


registrar(produto="Tomate", caixas=12)
