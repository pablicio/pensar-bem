import httpx


async def cotacao_do_dia() -> Decimal:
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get("https://api.exemplo/cotacao")
        r.raise_for_status()
        return Decimal(str(r.json()["valor"]))
