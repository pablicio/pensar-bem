import pandas as pd

cadernos = pd.read_csv("dados/brutos/cadernos.csv",
                       parse_dates=["data_hora"],
                       index_col="data_hora")
leitura = cadernos["leitura_cm"]
passo = leitura.index.to_series().diff()
print("intervalo entre leituras seguidas:")
print(passo.value_counts().head(4).to_string())
horaria = leitura.asfreq("h")
falta = horaria.isna()
bloco = (falta != falta.shift()).cumsum()[falta]
tamanhos = bloco.value_counts()
depois = horaria.index[falta] >= "1996-07-01"
print("lacunas depois de julho de 1996:",
      bloco[depois].nunique())
grandes = tamanhos[tamanhos > 24]
for b, horas in grandes.items():
    inicio = bloco[bloco == b].index[0]
    print(f"lacuna de {horas} h desde {inicio:%d/%m/%Y %Hh}")
