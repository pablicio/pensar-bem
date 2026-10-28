from typing import Protocol


class Canal(Protocol):
    def enviar(self, texto: str) -> None:
        ...


def notificar(canal: Canal, texto: str) -> None:
    canal.enviar(texto)
