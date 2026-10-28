texto = "228.566,168"
kwh = float(texto.replace(".", "").replace(",", "."))
reais = round(kwh * 0.9412, 2)
troca = str.maketrans(",.", ".,")
print(f"{kwh} kWh")
print("R$ " + f"{reais:,.2f}".translate(troca))
