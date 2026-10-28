import pandas as pd

from rio.plantao import COTA

rio = pd.read_csv("simulado_rio.csv", index_col="hora",
                  parse_dates=["hora"])
teto = rio["teto"]
for horas in (1, 3, 6):
    # desliga só depois de `horas` rodadas seguidas abaixo
    abaixo = (teto < COTA).rolling(horas).sum() == horas
    ligado, sms = False, []
    for h in rio.index:
        if not ligado and teto[h] >= COTA:
            ligado = True
            sms.append(f"liga {h:%d/%m %Hh}")
        elif ligado and abaixo[h]:
            ligado = False
            sms.append(f"desliga {h:%d/%m %Hh}")
    print(f"desligar depois de {horas} h abaixo da cota:")
    for i in range(0, len(sms), 3):
        print("   ", ", ".join(sms[i:i + 3]))
