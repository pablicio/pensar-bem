    try:
        with conectar() as conexao, conexao.cursor() as cur:
            cur.execute(...)
            return {"id": cur.fetchone()[0], **r.model_dump()}
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(409, "assento já reservado")
