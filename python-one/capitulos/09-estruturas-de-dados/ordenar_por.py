produtos = [
    {"nome": "Tomate", "preco": 8.90},
    {"nome": "Alface", "preco": 3.50},
]

por_preco = sorted(produtos, key=lambda p: p["preco"])
por_nome = sorted(produtos, key=lambda p: p["nome"])
