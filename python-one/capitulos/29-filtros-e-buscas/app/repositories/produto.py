def listar(
    self, filtro: ProdutoFiltro, limite: int, deslocamento: int
) -> list[Produto]:
    stmt = select(Produto)
    stmt = self._aplicar_filtros(stmt, filtro)
    stmt = self._aplicar_ordem(stmt, filtro)
    return list(
        self.session.scalars(
            stmt.limit(limite).offset(deslocamento)
        )
    )


def contar(self, filtro: ProdutoFiltro) -> int:
    stmt = select(func.count()).select_from(Produto)
    stmt = self._aplicar_filtros(stmt, filtro)
    return self.session.scalar(stmt) or 0


def _aplicar_filtros(self, stmt, filtro: ProdutoFiltro):
    if filtro.q:
        stmt = stmt.where(Produto.nome.ilike(f"%{filtro.q}%"))
    if filtro.categoria is not None:
        stmt = stmt.where(Produto.categoria == filtro.categoria)
    if filtro.preco_min is not None:
        stmt = stmt.where(Produto.preco >= filtro.preco_min)
    if filtro.preco_max is not None:
        stmt = stmt.where(Produto.preco <= filtro.preco_max)
    if filtro.apenas_disponiveis:
        stmt = stmt.where(Produto.estoque > 0)
    return stmt
