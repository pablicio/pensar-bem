import hashlib
from pathlib import Path

brutos = Path("dados/brutos")
for arquivo in sorted(brutos.glob("*.csv")):
    resumo = hashlib.sha256(arquivo.read_bytes()).hexdigest()
    print(resumo[:16], arquivo.name)
