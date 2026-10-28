import csv
from pathlib import Path

brutos = Path("dados/brutos")
envio = brutos / "envios" / "rateio_2027-02.csv"

# o mesmo arquivo lido com a tabela certa e com a errada
certo = envio.read_text(encoding="utf-8").splitlines()
errado = envio.read_text(encoding="latin-1").splitlines()
print(certo[200].split(";")[1], "|", errado[200].split(";")[1])
nomes = [linha.split(";")[1] for linha in errado[1:]]
quebrados = [nome for nome in nomes if "Ã" in nome]
print(len(quebrados), "de", len(nomes), "nomes quebrados")

# a compensação da GED: Latin-1 na entrada, UTF-8 na saída
origem = brutos / "ged/compensacao/compensacao_2027-02.csv"
destino = Path("dados/processados") / origem.name
destino.parent.mkdir(parents=True, exist_ok=True)
with open(origem, encoding="latin-1", newline="") as entrada, \
        open(destino, "w", encoding="utf-8",
             newline="") as saida:
    leitor = csv.reader(entrada, delimiter=";")
    escritor = csv.writer(saida, delimiter=";",
                          lineterminator="\n")
    for linha in leitor:
        escritor.writerow(linha)
print(destino.name, destino.stat().st_size, "bytes")
print(destino.read_text(encoding="utf-8").splitlines()[2])
