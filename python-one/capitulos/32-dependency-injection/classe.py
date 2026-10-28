class Paginacao:
    def __init__(self, pagina: int = 1, tamanho: int = 20):
        self.pagina = max(1, pagina)
        self.tamanho = max(1, min(tamanho, 100))

    @property
    def deslocamento(self) -> int:
        return (self.pagina - 1) * self.tamanho


PaginacaoDep = Annotated[Paginacao, Depends(Paginacao)]
