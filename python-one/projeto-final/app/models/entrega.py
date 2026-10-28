class StatusEntrega(str, Enum):
    PENDENTE = "pendente"
    CONFERIDA = "conferida"
    RECUSADA = "recusada"


class Entrega(Base):
    __tablename__ = "entrega"

    id: Mapped[int] = mapped_column(primary_key=True)
    produtor_id: Mapped[int] = mapped_column(
        ForeignKey("produtor.id"), index=True
    )
    data: Mapped[date] = mapped_column(index=True)
    status: Mapped[StatusEntrega] = mapped_column(
        default=StatusEntrega.PENDENTE, index=True
    )
    motivo_recusa: Mapped[str | None] = mapped_column(
        String(300), default=None
    )
    conferida_por: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id"), default=None
    )
    conferida_em: Mapped[datetime | None] = mapped_column(
        default=None
    )
    itens: Mapped[list["ItemEntrega"]] = relationship(
        back_populates="entrega", cascade="all, delete-orphan"
    )
