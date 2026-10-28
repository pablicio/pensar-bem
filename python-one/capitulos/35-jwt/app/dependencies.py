from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")


def usuario_atual(
    token: Annotated[str, Depends(oauth2)],
    servico: UsuarioServicoDep,
) -> Usuario:
    credenciais_invalidas = HTTPException(
        status_code=401,
        detail="credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        usuario_id = ler_token(token)
    except TokenInvalido as erro:
        raise credenciais_invalidas from erro

    usuario = servico.buscar(usuario_id)
    if usuario is None or not usuario.ativo:
        raise credenciais_invalidas

    return usuario


UsuarioDep = Annotated[Usuario, Depends(usuario_atual)]
