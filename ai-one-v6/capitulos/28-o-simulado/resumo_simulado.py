import numpy as np
import pandas as pd

HORA = pd.Timedelta("1h")
rio = pd.read_csv("simulado_rio.csv", index_col="hora",
                  parse_dates=["hora"])
msg = pd.read_csv("simulado_mensagens.csv",
                  parse_dates=["data_hora"])
tocou = rio.index[rio["alarme"]]
passou = rio.index[rio["nivel"] >= 5.5][0]
print(f"rio acima de 5,5 m: {passou:%d/%m %Hh}")
print(f"  primeiro alarme: {tocou[0]:%d/%m %Hh},"
      f" {(passou - tocou[0]) / HORA:.0f} h antes")
for hora, nota in rio["nota"].dropna().items():
    print(f"  {hora:%d/%m %Hh} SMS: {nota[:40]}")
fora = rio.index[rio["fora"].notna()]
print(f"Apiúna fora: {fora[0]:%d/%m %Hh}"
      f" a {fora[-1]:%d/%m %Hh}")
chamou = rio.index[rio["chamada"]]
print(f"chamadas ao Major: {len(chamou)},"
      f" de {chamou[0]:%d/%m %Hh} a {chamou[-1]:%d/%m %Hh}")
boato = msg["verdade"] == "boato"
print(f"mensagens: {len(msg)}; na pilha dos boatos"
      f" {msg['pilha'].sum()}")
intrusas = (msg["pilha"] & ~boato).sum()
print(f"  na pilha sem ser boato: {intrusas}")
risco = msg[msg["verdade"] == "risco"]
for coluna in ("espera_chegada", "espera_triagem"):
    w = risco[coluna]
    nome = coluna.replace("_", " por ")
    print(f"risco, {nome}: {w.median():.0f} min (mediana),"
          f" {w.max():.0f} (máx.)")
pedidos = msg["suspeito"].notna()
print(f"registros para a planilha: {pedidos.sum()},"
      f" {msg.loc[pedidos, 'suspeito'].mean():.0%} suspeitos")
