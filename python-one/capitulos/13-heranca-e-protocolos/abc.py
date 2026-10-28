from abc import ABC, abstractmethod


class Canal(ABC):
    @abstractmethod
    def enviar(self, texto: str) -> None:
        ...


class Email(Canal):
    def enviar(self, texto: str) -> None:
        print(f"e-mail: {texto}")
