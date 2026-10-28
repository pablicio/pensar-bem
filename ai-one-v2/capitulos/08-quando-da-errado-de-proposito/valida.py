from validacao import CPFInvalido, confere_cpf

caminho = "dados/brutos/ged/consumo/consumo_2027-02.csv"
rejeitadas = []
total_kwh = 0.0
lidas = 0
with open(caminho, encoding="utf-8") as entrada:
    entrada.readline()                  # o cabeçalho
    for numero, linha in enumerate(entrada, start=1):
        lidas += 1
        data, cpf, kwh = linha.strip().split(",")
        try:
            confere_cpf(cpf)
            total_kwh += float(kwh)
        except (CPFInvalido, ValueError) as erro:
            rejeitadas.append((numero, str(erro)))

print(f"{lidas} linhas lidas, {len(rejeitadas)} rejeitadas")
for numero, motivo in rejeitadas:
    print(f"  linha {numero}: {motivo}")
print(f"consumo de fevereiro: {total_kwh:,.2f} kWh")
