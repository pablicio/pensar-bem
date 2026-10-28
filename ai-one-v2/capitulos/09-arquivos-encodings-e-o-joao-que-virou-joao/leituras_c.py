import csv

pasta = "dados/brutos/inversores/abadiania/"
caminho = pasta + "abadiania_2027-02.csv"
contagem = {}
with open(caminho, encoding="utf-8-sig", newline="") as f:
    for linha in csv.DictReader(f):
        inversor = linha["inverter"]
        contagem[inversor] = contagem.get(inversor, 0) + 1
for inversor in list(contagem)[:3]:
    print(inversor, contagem[inversor])
print(len(contagem), "inversores,", sum(contagem.values()),
      "leituras")
