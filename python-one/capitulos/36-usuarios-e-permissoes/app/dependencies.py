from collections.abc import Callable


def exigir_papel(*papeis: Papel) -> Callable:
    def verificar(usuario: UsuarioDep) -> Usuario:
        if usuario.papel not in papeis:
            raise HTTPException(
                403, "você não tem permissão para esta operação"
            )
        return usuario

    return verificar


AdminDep = Annotated[
    Usuario, Depends(exigir_papel(Papel.ADMIN))
]
OperacaoDep = Annotated[
    Usuario, Depends(exigir_papel(Papel.ADMIN, Papel.OPERADOR))
]
