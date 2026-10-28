from sqlalchemy import Column, Table

produto_tag = Table(
    "produto_tag",
    Base.metadata,
    Column(
        "produto_id", ForeignKey("produto.id"), primary_key=True
    ),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(40), unique=True)


class Produto(Base):
    tags: Mapped[list[Tag]] = relationship(
        secondary=produto_tag, back_populates="produtos"
    )
