from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagina(BaseModel, Generic[T]):
    itens: list[T]
    total: int
    pagina: int
    tamanho: int

    @property
    def paginas(self) -> int:
        if self.tamanho == 0:
            return 0
        return -(-self.total // self.tamanho)
