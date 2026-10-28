import pandas as pd

from rateio.leitura import ler_abadiania

c = ler_abadiania("2027-02")
hora = pd.to_datetime(c["timestamp"]).dt.hour
com_sol = c["energy_kwh"] > 0
print("primeira hora com geração:", hora[com_sol].min())
print("última hora com geração:  ", hora[com_sol].max())
