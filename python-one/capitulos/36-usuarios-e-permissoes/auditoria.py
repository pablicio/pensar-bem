class Produto(Base):
    criado_por: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id"), default=None
    )
    atualizado_por: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id"), default=None
    )
