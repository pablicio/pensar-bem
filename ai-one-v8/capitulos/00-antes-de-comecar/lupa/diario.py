"""Ler os diários gerados no apêndice A3."""
import json
import textwrap
from pathlib import Path

BRUTOS = Path(__file__).parent.parent / "dados" / "brutos"


def le(nome):
    """Os registros de um arquivo .jsonl, numa lista."""
    with open(BRUTOS / nome, encoding="utf-8") as f:
        return [json.loads(linha) for linha in f]


def atos(nome="atos.jsonl"):
    return le(nome)


def gabarito():
    """A verdade de cada ato, pelo identificador."""
    return {g["id"]: g for g in le("gabarito.jsonl")}


def mostra(texto, largura=62):
    """Imprime um ato quebrando as linhas longas."""
    for linha in texto.split("\n"):
        print(textwrap.fill(linha, largura))
