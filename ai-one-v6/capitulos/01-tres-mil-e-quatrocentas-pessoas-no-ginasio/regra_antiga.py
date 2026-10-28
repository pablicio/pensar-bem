import pandas as pd

cadernos = pd.read_csv("dados/brutos/cadernos.csv",
                       parse_dates=["data_hora"],
                       index_col="data_hora")
nivel = cadernos["leitura_cm"].loc["1996-07-01":] / 100
nivel = nivel.asfreq("h")    # uma linha por hora; NaN na falta
subida = nivel.diff()        # metros por hora
dispara = (subida > 0.30).rolling(3).sum() == 3
ALERTA = 5.5
DIA = pd.Timedelta("24h")

alarmes = []
for hora in nivel.index[dispara]:
    if alarmes and hora - alarmes[-1] < DIA:
        continue             # o mesmo evento
    alarmes.append(hora)
print("disparos desde julho de 1996:", len(alarmes))
for hora in alarmes:
    pico = nivel.loc[hora:hora + DIA].max()
    veio = "passou do alerta" if pico >= ALERTA else "falso"
    print(f"  {hora:%d/%m/%Y %Hh}  pico em 24 h: {pico:5.2f} m"
          f"  {veio}")

# acima do alerta duas horas seguidas: leitura solta não conta
acima = (nivel >= ALERTA).rolling(2).sum() == 2
cheias, ultima = [], None
for hora in nivel.index[acima]:
    if ultima is None or hora - ultima > pd.Timedelta("72h"):
        cheias.append(hora)       # uma cheia nova
    ultima = hora
print("cheias acima do alerta:", len(cheias))
for hora in cheias:
    antes = [a for a in alarmes if hora - DIA <= a <= hora]
    aviso = "com alarme" if antes else "sem alarme nenhum"
    print(f"  {hora:%d/%m/%Y %Hh}  {aviso}")
