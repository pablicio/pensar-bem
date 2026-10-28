categoria = produto.get("categoria")
categoria = produto.get("categoria", "sem categoria")

if "categoria" in produto:
    categoria = produto["categoria"]
