import textwrap
import time

import pandas as pd
import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.plantao import Plantao
from rio.serie import ler, nivel_cidade

# a telemetria de janeiro de 2024 no formato da telemetria nova
tele = ler("telemetria").loc["2023-12-28":"2024-01-09"].copy()
tele["nivel_cidade"] = nivel_cidade().loc[tele.index] * 100
historico = com_subidas(tabela())
modelo = Previsor(historico.shape[1], range(36), estado=64)
modelo.load_state_dict(torch.load("plantao.pt"))
plantao = Plantao(modelo, Escala(historico), historico)
linhas, mais_lenta = [], 0.0
for agora in pd.date_range("2024-01-03", "2024-01-09 23:00",
                           freq="h"):
    inicio = time.time()
    linhas.append(plantao.hora(tele.loc[:agora]))
    mais_lenta = max(mais_lenta, time.time() - inicio)
registro = pd.DataFrame(linhas).set_index("hora")
registro.to_csv("registro_plantao.csv")
print(f"{len(registro)} rodadas, a mais lenta em"
      f" {mais_lenta * 1000:.0f} ms")
notas = registro["nota"]
mudou = notas.ne(notas.shift()) & notas.ne("")
for hora, l in registro[mudou].iterrows():
    vezes = (notas.loc[hora:] == l["nota"]).cumprod().sum()
    teto = ("" if pd.isna(l["teto"])
            else f", teto {l['teto']:.2f} m")
    print(f"{hora:%d/%m %Hh}  nível {l['nivel']:.2f} m{teto}")
    nota = l["nota"] + (f" ({vezes} h)" if vezes > 1 else "")
    print(textwrap.fill(nota, 60, initial_indent="    ",
                        subsequent_indent="    "))
tocando = registro.index[registro["alarme"]]
print(f"alarme de {tocando[0]:%d/%m %Hh}"
      f" a {tocando[-1]:%d/%m %Hh}")
acima = registro[registro["nivel"] >= 5.5]
print(f"o rio passou de 5,5 m às {acima.index[0]:%d/%m %Hh};"
      f" pico de {registro['nivel'].max():.2f} m")
print("chamadas ao Major:",
      [f"{h:%d/%m %Hh}" for h in registro.index[
          registro["chamada"]]])
