from enum import Enum


class Papel(str, Enum):
    ADMIN = "admin"
    OPERADOR = "operador"
    PRODUTOR = "produtor"


class Usuario(Base):
    papel: Mapped[Papel] = mapped_column(
        default=Papel.PRODUTOR
    )
    produtor_id: Mapped[int | None] = mapped_column(
        ForeignKey("produtor.id"), default=None
    )
