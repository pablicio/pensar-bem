from sqlalchemy.orm import selectinload

stmt = (
    select(Produto)
    .options(selectinload(Produto.produtor))
    .limit(100)
)
produtos = session.scalars(stmt).all()
