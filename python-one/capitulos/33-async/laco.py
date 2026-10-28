import asyncio


async def cozinhar(prato: str, minutos: int) -> str:
    print(f"começando {prato}")
    await asyncio.sleep(minutos)
    print(f"{prato} pronto")
    return prato


async def main() -> None:
    await asyncio.gather(
        cozinhar("arroz", 2),
        cozinhar("feijão", 3),
        cozinhar("salada", 1),
    )


asyncio.run(main())
