import pandas as pd

from rio.avalia import parte

cadernos = pd.read_csv("dados/brutos/cadernos.csv",
                       parse_dates=["data_hora"],
                       index_col="data_hora")
nivel = cadernos["leitura_cm"].loc["1996-07-01":] / 100
nivel = nivel[nivel < 14].asfreq("h")
teste = parte(nivel, "teste")
# o pico de cada cheia que passou do alerta: o máximo de cada
# trecho acima de 5,5 m (uma leitura que falta não o corta)
acima = teste.interpolate(limit=3) >= 5.5
trecho = (acima != acima.shift()).cumsum()[acima]
picos = teste[acima].groupby(trecho).idxmax()
print("pico                 nível   erro da persistência (m)")
print("                              1 h     6 h    12 h")
for hora in picos:
    real = teste[hora]
    erros = [teste[hora - pd.Timedelta(h, "h")] - real
             for h in (1, 6, 12)]
    print(f"{hora:%d/%m/%Y %Hh}  {real:6.2f}  "
          + "  ".join(f"{e:6.2f}" for e in erros))
