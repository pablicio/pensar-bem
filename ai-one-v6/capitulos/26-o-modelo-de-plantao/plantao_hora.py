"""Uma rodada do plantão, que o servidor roda toda hora."""
import sys
from pathlib import Path

import pandas as pd
import torch

from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.plantao import Plantao
from rio.serie import ler

REGISTRO = Path("registro_temporada.csv")
tele = ler("temporada_2027")
agora = pd.Timestamp(sys.argv[1]) if len(sys.argv) > 1 \
    else tele.index[-1]
historico = com_subidas(tabela())
modelo = Previsor(historico.shape[1], range(36), estado=64)
modelo.load_state_dict(torch.load("plantao.pt"))
plantao = Plantao(modelo, Escala(historico), historico)
linha = plantao.hora(tele.loc[:agora])
pd.DataFrame([linha]).set_index("hora").round(2).to_csv(
    REGISTRO, mode="a", header=not REGISTRO.exists())
hora, nivel = linha["hora"], linha["nivel"]
print(f"{hora:%d/%m/%Y %Hh}: nível {nivel:.2f} m")
if linha["teto"] is not None:
    print(f"  em 12 h: mediana {linha['mediana']:.2f} m,"
          f" teto {linha['teto']:.2f} m")
    print(f"  alarme: {linha['alarme']}")
print("  " + (linha["nota"] or "sem aviso"))
