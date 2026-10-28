taxa_ano = (9000 / 2400) ** (1 / 7) - 1
taxa_mes = (1 + taxa_ano) ** (1 / 12) - 1

valor = 2400.0
meses = 0
while valor < 2 * 2400:
    valor = valor * (1 + taxa_mes)
    meses += 1

print(f"taxa ao mês: {taxa_mes * 100:.3f}%")
print(f"dobrou em {meses} meses ({meses / 12:.2f} anos)")
print(f"regra do 72: {72 / (taxa_ano * 100):.2f} anos")
