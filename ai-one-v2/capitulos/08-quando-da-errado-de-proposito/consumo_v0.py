from funcoes import normaliza_cpf

caminho = "dados/brutos/ged/consumo/consumo_2027-02.csv"
total = 0.0
with open(caminho, encoding="utf-8") as entrada:
    entrada.readline()                  # pula o cabeçalho
    for linha in entrada:
        data, cpf, kwh = linha.strip().split(",")
        chave = int(normaliza_cpf(cpf))
        total += float(kwh)
print(total)
