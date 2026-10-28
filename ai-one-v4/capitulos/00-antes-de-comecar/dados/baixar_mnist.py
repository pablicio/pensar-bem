"""Baixa o MNIST uma vez e confere cada arquivo."""
import hashlib
import urllib.request
from pathlib import Path

ESPELHO = "https://ossci-datasets.s3.amazonaws.com/mnist/"
PASTA = Path("dados/brutos/mnist")
ARQUIVOS = {
    "train-images-idx3-ubyte.gz": (
        "440fcabf73cc546fa21475e81ea37026"
        "5605f56be210a4024d2ca8f203523609"),
    "train-labels-idx1-ubyte.gz": (
        "3552534a0a558bbed6aed32b30c495cc"
        "a23d567ec52cac8be1a0730e8010255c"),
    "t10k-images-idx3-ubyte.gz": (
        "8d422c7b0a1c1c79245a5bcf07fe86e3"
        "3eeafee792b84584aec276f5a2dbc4e6"),
    "t10k-labels-idx1-ubyte.gz": (
        "f7ae60f92e00ec6debd23a6088c31dbd"
        "2371eca3ffa0defaefb259924204aec6"),
}

PASTA.mkdir(parents=True, exist_ok=True)
for nome, esperado in ARQUIVOS.items():
    destino = PASTA / nome
    if not destino.exists():
        urllib.request.urlretrieve(ESPELHO + nome, destino)
    resumo = hashlib.sha256(destino.read_bytes()).hexdigest()
    if resumo != esperado:
        destino.unlink()
        raise SystemExit(f"{nome}: o arquivo não confere")
    print(f"ok  {nome}  {destino.stat().st_size:>10,} bytes")
