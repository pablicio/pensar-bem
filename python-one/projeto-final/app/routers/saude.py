@router.get("/saude")
def vivo():
    return {"status": "de pé"}


@router.get("/pronto")
def pronto(session: SessaoDep):
    try:
        session.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(503, "banco indisponível")
    return {"status": "pronto"}
