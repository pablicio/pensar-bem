"""Registro de experimentos: uma linha por rodada."""
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

from rateio import __version__
from rateio.manifesto import sha256

REGISTRO = Path("experimentos/registro.csv")
CAMPOS = ["quando", "experimento", "versao_rateio", "entradas",
          "parametros", "metricas"]


def hash_das_entradas(arquivos):
    """Um SHA-256 só, feito dos SHA-256 de cada arquivo."""
    caminhos = sorted(Path(a).as_posix() for a in arquivos)
    texto = "\n".join(f"{sha256(c)}  {c}" for c in caminhos)
    return hashlib.sha256(texto.encode()).hexdigest()


def registrar(experimento, parametros, metricas, arquivos):
    """Acrescenta uma rodada ao fim do registro."""
    REGISTRO.parent.mkdir(exist_ok=True)
    novo = not REGISTRO.exists()
    agora = datetime.now().isoformat(timespec="seconds")
    linha = {"quando": agora,
             "experimento": experimento,
             "versao_rateio": __version__,
             "entradas": hash_das_entradas(arquivos),
             "parametros": json.dumps(parametros),
             "metricas": json.dumps(metricas)}
    with REGISTRO.open("a", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS)
        if novo:
            escritor.writeheader()
        escritor.writerow(linha)
