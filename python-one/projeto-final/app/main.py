from fastapi import FastAPI

from app.config import get_config
from app.routers import produtos

config = get_config()

app = FastAPI(
    title=config.app_nome,
    version="0.1.0",
    summary="API do catálogo da Cooperativa Sabiá",
)

app.include_router(produtos.router)


@app.get("/saude", tags=["infra"])
def saude():
    return {"status": "de pé", "ambiente": config.app_ambiente}
