import hashlib


def hash_refresh(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def criar_par(
    usuario_id: int, servico: UsuarioServicoDep
) -> dict[str, str]:
    refresh = criar_refresh(usuario_id, dias=14)
    servico.guardar_refresh(
        usuario_id=usuario_id,
        hash_token=hash_refresh(refresh),
    )
    return {
        "access_token": criar_token(usuario_id, minutos=30),
        "refresh_token": refresh,
        "token_type": "bearer",
    }


@router.post("/renovar")
def renovar(dados: RenovarEntrada, servico: UsuarioServicoDep):
    usuario_id = ler_refresh(dados.refresh_token)
    sessao = servico.consumir_refresh(
        usuario_id, hash_refresh(dados.refresh_token)
    )
    if sessao is None:
        raise HTTPException(401, "sessão encerrada")
    # Consumir invalida o token anterior antes de emitir o próximo.
    return criar_par(usuario_id, servico)
