@router.get("/saude")
async def saude(db=Depends(conexao), cache=Depends(redis)):
    await db.execute("SELECT 1")
    await cache.ping()
    return {"ok": True, "versao": VERSAO}
