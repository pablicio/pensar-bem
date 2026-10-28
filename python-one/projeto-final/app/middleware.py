@app.middleware("http")
async def correlacao(request: Request, call_next):
    rid = request.headers.get("X-Request-Id") or uuid.uuid4().hex
    request.state.request_id = rid

    resposta = await call_next(request)
    resposta.headers["X-Request-Id"] = rid
    return resposta
