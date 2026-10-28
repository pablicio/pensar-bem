import logging
import sys


def configurar_log(nivel: str = "INFO") -> None:
    logging.basicConfig(
        level=nivel,
        stream=sys.stdout,
        format=(
            '{"hora":"%(asctime)s","nivel":"%(levelname)s",'
            '"origem":"%(name)s","msg":"%(message)s"}'
        ),
    )
