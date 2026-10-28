"""Manifesto: o SHA-256 de cada arquivo de uma pasta."""
import hashlib
import json
from pathlib import Path

from rateio import __version__

BLOCO = 1024 * 1024          # lê de 1 MB em 1 MB


def sha256(caminho):
    """O SHA-256 de um arquivo, em hexadecimal."""
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        while bloco := f.read(BLOCO):
            h.update(bloco)
    return h.hexdigest()


def gerar(pasta):
    """{caminho relativo: SHA-256} de cada arquivo da pasta."""
    pasta = Path(pasta)
    return {p.relative_to(pasta).as_posix(): sha256(p)
            for p in sorted(pasta.rglob("*")) if p.is_file()}


def gravar(manifesto, destino):
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(manifesto, f, indent=1, sort_keys=True)


def ler(origem):
    with open(origem, encoding="utf-8") as f:
        return json.load(f)


def comparar(antes, agora):
    """O que mudou de um manifesto para outro."""
    comuns = antes.keys() & agora.keys()
    return {"alterados": sorted(k for k in comuns
                                if antes[k] != agora[k]),
            "faltando": sorted(antes.keys() - agora.keys()),
            "novos": sorted(agora.keys() - antes.keys())}


def registrar_origem(saida, entradas, programa):
    """Grava, ao lado de um resultado, de onde ele veio."""
    origem = {"saida": Path(saida).as_posix(),
              "sha256": sha256(saida),
              "programa": programa,
              "versao_rateio": __version__,
              "entradas": {Path(e).as_posix(): sha256(e)
                           for e in entradas}}
    gravar(origem, f"{saida}.origem.json")
    return origem
