from rateio.leitura import ler_corumba

meses = ["2026-03", "2026-04", "2026-05", "2026-06", "2026-07",
         "2026-08", "2026-09", "2026-10", "2026-11", "2026-12",
         "2027-01", "2027-02"]
for mes in meses:
    maximo = ler_corumba(mes).groupby("Data")["Energia"].max()
    suspeitos = int((maximo < 10).sum())
    print(mes, suspeitos, "dias suspeitos")
