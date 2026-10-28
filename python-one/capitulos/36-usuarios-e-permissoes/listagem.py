def listar(
    self, filtro: ProdutoFiltro, usuario: Usuario
) -> list[Produto]:
    if usuario.papel is Papel.PRODUTOR:
        filtro = filtro.model_copy(
            update={"produtor_id": usuario.produtor_id}
        )
    return self.repo.listar(filtro)
