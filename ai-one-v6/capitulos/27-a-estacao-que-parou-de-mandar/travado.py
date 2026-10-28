import pandas as pd

from rio.avalia import parte
from rio.cota import grupos
from rio.estacoes import ESTACOES, TRAVADA
from rio.serie import ler

HORA = pd.Timedelta("1h")
tele = ler("telemetria")
for estacao in ESTACOES:
    s = tele[f"nivel_{estacao}"]
    parada = s.diff().eq(0)
    # quantas horas seguidas sem mudar, terminando em cada hora
    seguidas = parada.groupby((~parada).cumsum()).cumsum()
    maior = parte(seguidas, "treino").max()
    print(f"{estacao}: no treino, até {maior} h sem mudar")
    marcada = seguidas >= TRAVADA - 1
    for inicio, fim in grupos(marcada.index[marcada], "1h"):
        parou = fim - int(seguidas[fim]) * HORA
        demora = (inicio - parou) / HORA
        print(f"  parada em {parou:%d/%m/%Y %Hh}, marcada"
              f" {demora:.0f} h depois, até {fim:%d/%m %Hh}")
