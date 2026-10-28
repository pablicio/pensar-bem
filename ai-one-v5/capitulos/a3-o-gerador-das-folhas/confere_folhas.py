import hashlib
from pathlib import Path

PASTA = Path("dados/brutos")
for nome in ["fotos", "mascaras", "lesoes"]:
    resumo = hashlib.sha256()
    arquivos = sorted((PASTA / nome).iterdir())
    for arquivo in arquivos:
        resumo.update(arquivo.read_bytes())
    print(resumo.hexdigest()[:16], nome, len(arquivos),
          "arquivos")
for nome in ["fotos.csv", "caixas.csv", "revisao.csv"]:
    resumo = hashlib.sha256((PASTA / nome).read_bytes())
    print(resumo.hexdigest()[:16], nome)
