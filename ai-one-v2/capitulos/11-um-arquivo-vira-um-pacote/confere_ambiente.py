from importlib.metadata import version
from pathlib import Path

linhas = Path("requirements.txt").read_text().splitlines()
for linha in linhas:
    nome, fixada = linha.split("==")
    instalada = version(nome)
    marca = "ok" if instalada == fixada else "DIFERENTE"
    print(f"{nome:12} {fixada:8} {instalada:8} {marca}")
