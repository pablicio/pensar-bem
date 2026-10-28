from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Produtor(Base):
    __tablename__ = "produtor"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    cidade: Mapped[str] = mapped_column(String(100))

    produtos: Mapped[list["Produto"]] = relationship(
        back_populates="produtor",
        cascade="all, delete-orphan",
    )


class Produto(Base):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    produtor_id: Mapped[int] = mapped_column(
        ForeignKey("produtor.id"), index=True
    )

    produtor: Mapped["Produtor"] = relationship(
        back_populates="produtos"
    )
