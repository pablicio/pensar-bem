with SessionLocal() as session:
    produto = session.get(Produto, 1)
    if produto is None:
        raise ValueError("não existe")

    produto.preco = Decimal("9.50")
    session.commit()
