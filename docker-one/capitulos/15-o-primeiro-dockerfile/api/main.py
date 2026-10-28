from fastapi import FastAPI

app = FastAPI()

EVENTOS = [
    {"id": 1, "nome": "Festival de Inverno da Serra 2027",
     "lugares": 18000},
]


@app.get("/eventos")
def listar_eventos() -> list[dict]:
    return EVENTOS
