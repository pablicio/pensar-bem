"""Roda as células de rateio.ipynb numa ordem dada."""
import json
import random
import sys


def celulas(caminho):
    with open(caminho, encoding="utf-8") as f:
        notebook = json.load(f)
    return ["".join(c["source"]) for c in notebook["cells"]]


def roda(ordem, semente=0):
    random.seed(semente)      # para o livro mostrar um número
    fontes = celulas("rateio.ipynb")
    kernel = {}               # as variáveis do "kernel"
    for n in ordem:
        exec(fontes[n - 1], kernel)
    return kernel


if __name__ == "__main__":
    roda([int(n) for n in sys.argv[1:]])
