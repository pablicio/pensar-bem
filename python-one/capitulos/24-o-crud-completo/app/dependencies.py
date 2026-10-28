from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.produto import ProdutoRepositorioSQL
from app.services.produto import ProdutoServico


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise


SessaoDep = Annotated[Session, Depends(get_session)]


def get_produto_servico(session: SessaoDep) -> ProdutoServico:
    return ProdutoServico(session, ProdutoRepositorioSQL(session))


ServicoDep = Annotated[ProdutoServico, Depends(get_produto_servico)]
