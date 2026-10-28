MAX_POR_SESSAO = int(os.environ.get("MAX_ASSENTOS_POR_SESSAO", "0"))

    if MAX_POR_SESSAO:
        conta = f"sessao:{p.sessao}:assentos"
        if cache.incr(conta) > MAX_POR_SESSAO:
            raise HTTPException(429, "limite de assentos por compra")
        cache.expire(conta, 600)
