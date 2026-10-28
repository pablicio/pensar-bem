from fastapi.security import OAuth2PasswordRequestForm


@router.post("/login")
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    servico: UsuarioServicoDep,
):
    usuario = servico.autenticar(form.username, form.password)
    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="e-mail ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"acesso": "ok", "usuario_id": usuario.id}
