from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.produto import Produto


class ProdutoRepositorioSQL:
    def __init__(self, session: Session):
        self.session = session

    def buscar(self, produto_id: int) -> Produto | None:
        return self.session.get(Produto, produto_id)

    def buscar_por_nome(self, nome: str) -> Produto | None:
        stmt = select(Produto).where(Produto.nome == nome)
        return self.session.scalars(stmt).first()

    def listar(
        self, limite: int = 20, deslocamento: int = 0
    ) -> list[Produto]:
        stmt = (
            select(Produto)
            .order_by(Produto.nome)
            .limit(limite)
            .offset(deslocamento)
        )
        return list(self.session.scalars(stmt))

    def contar(self) -> int:
        return self.session.scalar(
            select(func.count()).select_from(Produto)
        ) or 0

    def criar(self, produto: Produto) -> Produto:
        self.session.add(produto)
        self.session.flush()
        return produto

    def remover(self, produto: Produto) -> None:
        self.session.delete(produto)
