def listar(self, limite: int, deslocamento: int) -> list[Produto]:
    stmt = (
        select(Produto)
        .order_by(Produto.nome, Produto.id)
        .limit(limite)
        .offset(deslocamento)
    )
    return list(self.session.scalars(stmt))


def contar(self) -> int:
    return self.session.scalar(
        select(func.count()).select_from(Produto)
    ) or 0
