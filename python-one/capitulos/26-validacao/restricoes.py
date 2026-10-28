from sqlalchemy import CheckConstraint, UniqueConstraint


class Produto(Base):
    __tablename__ = "produto"
    __table_args__ = (
        UniqueConstraint("nome", name="uq_produto_nome"),
        CheckConstraint("preco > 0", name="ck_produto_preco"),
        CheckConstraint("estoque >= 0", name="ck_produto_estoque"),
    )
