import logging
import uuid

logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def _nao_tratado(request: Request, exc: Exception):
    incidente = uuid.uuid4().hex[:12]

    logger.exception(
        "erro nao tratado incidente=%s metodo=%s caminho=%s",
        incidente, request.method, request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "tipo": "erro_interno",
            "mensagem": (
                "Erro inesperado. Informe o código ao suporte."
            ),
            "incidente": incidente,
        },
    )
