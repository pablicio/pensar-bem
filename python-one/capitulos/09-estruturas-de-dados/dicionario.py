produto = {
    "nome": "Tomate italiano",
    "preco": 8.90,
    "estoque": 120,
}

print(produto["nome"])
produto["organico"] = True
del produto["estoque"]

for chave, valor in produto.items():
    print(f"{chave} = {valor}")
