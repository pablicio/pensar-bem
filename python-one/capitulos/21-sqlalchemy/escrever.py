from decimal import Decimal

from app.database import SessionLocal
from app.models.produto import Produto

with SessionLocal() as session:
    produto = Produto(
        nome="Cenoura", preco=Decimal("5.25"), estoque=60
    )

    session.add(produto)
    session.commit()

    print(produto.id)
