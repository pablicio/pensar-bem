from rateio.leitura import ler_corumba

a = ler_corumba("2027-02")
maximo = a.groupby("Data")["Energia"].max()
print(maximo.loc["06/02/2027":"13/02/2027"])
suspeitos = maximo[maximo < 10]
print("dias suspeitos:", list(suspeitos.index))
