def listar_apos(
    self, depois_de: int | None, limite: int
) -> list[Produto]:
    stmt = select(Produto).order_by(Produto.id).limit(limite)
    if depois_de is not None:
        stmt = stmt.where(Produto.id > depois_de)
    return list(self.session.scalars(stmt))
