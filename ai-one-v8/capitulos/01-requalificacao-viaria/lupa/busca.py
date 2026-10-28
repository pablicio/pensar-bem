"""A busca por palavras-chave da Lupa, como o Renan a fez."""
from pathlib import Path

LISTA = (Path(__file__).parent.parent / "dados" / "brutos"
         / "palavras_chave.txt")


def palavras_chave():
    return LISTA.read_text(encoding="utf-8").split("\n")[:-1]


def busca(atos, palavras):
    """Os atos em que aparece alguma palavra, e qual."""
    achados = []
    for ato in atos:
        for p in palavras:
            if p in ato["texto"]:
                achados.append((ato, p))
                break
    return achados
