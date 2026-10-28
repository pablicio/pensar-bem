class TokenInvalido(Exception):
    pass


def ler_token(token: str) -> int:
    try:
        carga = jwt.decode(
            token,
            get_config().secret_key,
            algorithms=[ALGORITMO],
        )
    except jwt.ExpiredSignatureError as erro:
        raise TokenInvalido("token expirado") from erro
    except jwt.InvalidTokenError as erro:
        raise TokenInvalido("token inválido") from erro

    if carga.get("typ") != "acesso":
        raise TokenInvalido("tipo de token incorreto")

    return int(carga["sub"])
