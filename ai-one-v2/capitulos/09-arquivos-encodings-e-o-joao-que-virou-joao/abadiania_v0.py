import csv

pasta = "dados/brutos/inversores/abadiania/"
caminho = pasta + "abadiania_2027-02.csv"
with open(caminho, encoding="utf-8", newline="") as entrada:
    leitor = csv.DictReader(entrada)
    primeira = next(leitor)
print(primeira["timestamp"])
