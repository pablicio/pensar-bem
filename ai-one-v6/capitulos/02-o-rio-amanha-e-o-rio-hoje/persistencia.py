import pandas as pd

from rio.avalia import mae, parte, rmse

cadernos = pd.read_csv("dados/brutos/cadernos.csv",
                       parse_dates=["data_hora"],
                       index_col="data_hora")
nivel = cadernos["leitura_cm"].loc["1996-07-01":] / 100
nivel = nivel[nivel < 14].asfreq("h")  # a régua vai até 14 m
teste = parte(nivel, "teste")
print("horizonte   MAE (cm)   RMSE (cm)")
for h in [1, 3, 6, 12, 24, 360]:
    erro = teste.shift(h) - teste        # previsto menos real
    print(f"{h:6d} h {mae(erro) * 100:10.1f}"
          f" {rmse(erro) * 100:11.1f}")
