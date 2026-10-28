"""python -m rateio --mes AAAA-MM: o rateio de um mês."""
import argparse
import logging
import re
import sys
import tomllib
from pathlib import Path

from rateio import __version__
from rateio.pipeline import DadosInesperados, rodar


def mes_valido(texto):
    """'AAAA-MM', ou o erro que o argparse mostra."""
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", texto):
        raise argparse.ArgumentTypeError(
            f"{texto!r} não é AAAA-MM")
    return texto


def le_argumentos(lista):
    p = argparse.ArgumentParser(
        prog="python -m rateio",
        description="O rateio de créditos da Coopersol.")
    p.add_argument("--mes", required=True, type=mes_valido,
                   help="o mês do rateio, como 2027-03")
    p.add_argument("--config", default="rateio.toml",
                   help="arquivo de configuração")
    p.add_argument("--version", action="version",
                   version=f"rateio {__version__}")
    return p.parse_args(lista)


def configura_log(arquivo):
    """Mensagens na tela e, com data e hora, no arquivo."""
    log = logging.getLogger("rateio")
    log.setLevel(logging.INFO)
    tela = logging.StreamHandler(sys.stdout)
    tela.setFormatter(logging.Formatter(
        "%(levelname)-7s %(message)s"))
    disco = logging.FileHandler(arquivo, encoding="utf-8")
    disco.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)-7s %(message)s"))
    log.addHandler(tela)
    log.addHandler(disco)
    return log


def main(lista):
    args = le_argumentos(lista)
    with open(args.config, "rb") as f:
        config = tomllib.load(f)
    pasta = Path(config["saida"]) / args.mes
    pasta.mkdir(parents=True, exist_ok=True)
    log = configura_log(pasta / "rateio.log")
    log.info("rateio %s, mês %s, %s", __version__, args.mes,
             args.config)
    try:
        rodar(args.mes, config)
    except DadosInesperados as erro:
        log.error("parado, nada foi gravado: %s", erro)
        return 1
    log.info("pronto")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
