from pathlib import Path

corumba = Path("dados/brutos/inversores/corumba")
for arquivo in sorted(corumba.glob("*.csv")):
    texto = arquivo.read_text()
    print(arquivo.name, texto.count("\n"))
