import hashlib
from pathlib import Path

PASTA = Path("dados/brutos")
for nome in ["telemetria.csv", "cadernos.csv",
             "temporada_2027.csv", "mensagens.csv"]:
    dados = (PASTA / nome).read_bytes()
    linhas = dados.count(b"\n") - 1
    resumo = hashlib.sha256(dados).hexdigest()[:16]
    print(f"{resumo}  {nome:20} {linhas:>8,} linhas")
