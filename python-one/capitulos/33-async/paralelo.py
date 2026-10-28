async def painel(client: httpx.AsyncClient) -> dict:
    cotacao, clima, feriados = await asyncio.gather(
        client.get("https://api.exemplo/cotacao"),
        client.get("https://api.exemplo/clima"),
        client.get("https://api.exemplo/feriados"),
    )
    return {
        "cotacao": cotacao.json(),
        "clima": clima.json(),
        "feriados": feriados.json(),
    }
