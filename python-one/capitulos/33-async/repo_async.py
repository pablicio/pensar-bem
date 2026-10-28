async def buscar(self, produto_id: int) -> Produto | None:
    return await self.session.get(Produto, produto_id)


async def listar(self, limite: int) -> list[Produto]:
    stmt = select(Produto).limit(limite)
    resultado = await self.session.scalars(stmt)
    return list(resultado)
