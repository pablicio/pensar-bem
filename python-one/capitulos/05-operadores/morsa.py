produtos = buscar_produtos()

if (total := len(produtos)) > 100:
    print(f"catálogo grande: {total} itens")
