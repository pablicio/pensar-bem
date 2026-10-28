import pandas as pd

cadernos = pd.read_csv("dados/brutos/cadernos.csv",
                       parse_dates=["data_hora"],
                       index_col="data_hora")
print(len(cadernos), "leituras, de", cadernos.index[0])
print("a", cadernos.index[-1])
print(cadernos.head(3))
nov = cadernos.loc["2008-11"]
print("maior leitura de novembro de 2008:",
      nov["leitura_cm"].max(), "cm")
print("em", nov["leitura_cm"].idxmax())
