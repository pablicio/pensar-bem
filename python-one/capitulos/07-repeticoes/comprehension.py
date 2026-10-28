precos = [8.90, 3.50, 12.00, 5.25]

com_margem = [p * 1.12 for p in precos]
caros = [p for p in precos if p > 10]
