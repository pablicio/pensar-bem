vendas = []
for s in range(26):
    vendas.append(120 * 0.5 ** (s / 2))
print(f"total: {sum(vendas):.0f} cópias")
print(f"semana 25: {vendas[25]:.2f} cópias")
