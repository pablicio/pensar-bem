produtos = [
    {"nome": "Tomate", "preco": 8.90, "categoria": "fruta"},
    {"nome": "Alface", "preco": 3.50, "categoria": "verdura"},
]

por_nome = {p["nome"]: p["preco"] for p in produtos}
categorias = {p["categoria"] for p in produtos}

print(por_nome)
print(sorted(categorias))
