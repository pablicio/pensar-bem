import numpy as np
import pandas as pd

from rio.alerta import maximo_previsto
from rio.avalia import parte
from rio.cota import grupos
from rio.entradas import Escala, com_subidas, tabela
from rio.reserva import fora_da_faixa
from rio.treino import conjunto

tab = com_subidas(tabela())
nivel = tab["cidade"]
H = tuple(range(1, 13))
escalada = Escala(tab).aplica(tab)
_, _, horas = conjunto(escalada, nivel, "teste", H)
agora = nivel.loc[horas].to_numpy()
maximo = maximo_previsto(agora, np.load("quantis.npy"), 2)
alarme = pd.Series(maximo >= 5.5, index=horas)
teste = parte(nivel, "teste")
print("alarme (quantil 95%)       duração  pico em 12 h")
for inicio, fim in grupos(alarme.index[alarme]):
    depois = teste.loc[inicio:fim + pd.Timedelta("12h")]
    veio = "cheia" if depois.max() >= 5.5 else "falso"
    horas_alarme = (fim - inicio) / pd.Timedelta("1h") + 1
    print(f"{inicio:%d/%m/%Y %Hh} a {fim:%d/%m %Hh}"
          f" {horas_alarme:5.0f} h {depois.max():6.2f} m"
          f"  {veio}")
fora = fora_da_faixa(tab).loc[horas]
subindo = (nivel.diff(3) > 0.3).loc[horas]
chamadas = grupos(horas[(fora & subindo).to_numpy()])
print("chamadas ao Major (fora da faixa e o rio subindo):",
      len(chamadas))
for inicio, _ in chamadas:
    print(f"  {inicio:%d/%m/%Y %Hh}")
