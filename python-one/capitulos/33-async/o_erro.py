@app.get("/relatorio")
async def relatorio():
    time.sleep(5)          # NÃO
    return {"ok": True}
