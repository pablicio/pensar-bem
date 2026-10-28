_CAMPOS = {
    "nome": Produto.nome,
    "preco": Produto.preco,
    "criado_em": Produto.criado_em,
}


def _aplicar_ordem(self, stmt, filtro: ProdutoFiltro):
    coluna = _CAMPOS[filtro.ordenar_por]
    if filtro.ordem == "desc":
        coluna = coluna.desc()
    return stmt.order_by(coluna, Produto.id)
