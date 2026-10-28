import logging

logger = logging.getLogger(__name__)

try:
    atualizar(produto)
except ErroDoCatalogo:
    logger.exception("falha ao atualizar produto %s", produto.id)
    raise
