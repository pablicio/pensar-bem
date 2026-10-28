import matplotlib.pyplot as plt
import pandas as pd

from rio.serie import REGUA_NOVA, ler

cidade = ler("cadernos")["leitura_cm"] / 100
apiuna = ler("telemetria")["nivel_apiuna"] / 100
juntas = pd.DataFrame({"cidade": cidade, "apiuna": apiuna})
juntas = juntas[juntas["cidade"] < 14].dropna()
diferenca = juntas["cidade"] - juntas["apiuna"]
ano = pd.DateOffset(years=1)
antes = diferenca.loc[REGUA_NOVA - ano:REGUA_NOVA].median()
depois = diferenca.loc[REGUA_NOVA:REGUA_NOVA + ano].median()
print(f"cidade menos Apiúna: {antes:+.2f} m no ano antes,"
      f" {depois:+.2f} m no ano depois")
print(f"o degrau: {depois - antes:.2f} m")

mensal = diferenca.resample("MS").median().loc["1993":"1999"]
fig, ax = plt.subplots(figsize=(6, 2.8))
ax.step(mensal.index, mensal, where="post", color="#2A5F9E")
ax.axvline(REGUA_NOVA, color="0.5", ls="--", lw=0.8)
ax.set_ylabel("cidade menos Apiúna (m)")
fig.tight_layout()
fig.savefig("degrau.png", dpi=300)
