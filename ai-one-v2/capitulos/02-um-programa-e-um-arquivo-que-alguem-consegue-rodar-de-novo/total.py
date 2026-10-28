usina = "Corumbá de Goiás"
dia = "08/02/2027"
# kWh de cada hora com sol, das 6h às 18h, ditados pelo Wesley
total = (88.9 + 304.5 + 561.9 + 682.4 + 969.1 + 998.5
         + 928.1 + 1026.9 + 842.3 + 691.4 + 444.1 + 211.0
         + 22.9)
horas_com_sol = 13
media = total / horas_com_sol
bateu_meta = total > 8000

print(f"{usina}, {dia}")
print(f"geração do dia: {total:.1f} kWh")
print(f"média por hora com sol: {media:.1f} kWh")
print(f"passou de 8.000 kWh? {bateu_meta}")
