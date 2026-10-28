from rateio import manifesto

caminho = "dados/processados/rateio_2027-02_corrigido.csv"
origem = manifesto.ler(caminho + ".origem.json")

problemas = []
if manifesto.sha256(origem["saida"]) != origem["sha256"]:
    problemas.append(origem["saida"])
for entrada, sha in origem["entradas"].items():
    if manifesto.sha256(entrada) != sha:
        problemas.append(entrada)

n = len(origem["entradas"])
if problemas:
    print("mudaram:", *problemas)
else:
    print(f"resultado e {n} entradas conferidos")
