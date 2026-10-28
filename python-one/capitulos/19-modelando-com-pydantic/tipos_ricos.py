from datetime import date

from pydantic import BaseModel, EmailStr, HttpUrl


class Produtor(BaseModel):
    nome: str
    email: EmailStr
    site: HttpUrl | None = None
    desde: date
