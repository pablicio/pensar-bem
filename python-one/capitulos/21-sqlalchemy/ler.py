from sqlalchemy import select

with SessionLocal() as session:
    # um, pela chave primária
    produto = session.get(Produto, 1)

    # um, por outro critério
    stmt = select(Produto).where(Produto.nome == "Cenoura")
    produto = session.scalars(stmt).first()

    # vários
    stmt = (
        select(Produto)
        .where(Produto.estoque > 0)
        .order_by(Produto.nome)
        .limit(20)
    )
    produtos = session.scalars(stmt).all()
