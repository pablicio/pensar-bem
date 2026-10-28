from rio.avalia import parte
from rio.entradas import NIVEIS, com_subidas, tabela
from rio.reserva import chuva_24h

tab = com_subidas(tabela())
cheia = slice("2008-11-20", "2008-11-24 12:00")
print("série              treino  2008   passou em")
for nome, serie in [*((n, tab[n]) for n in NIVEIS),
                    *chuva_24h(tab).items()]:
    teto = parte(serie, "treino").max()
    trecho = serie.loc[cheia]
    acima = trecho.index[trecho > teto]
    quando = f"{acima[0]:%d/%m %Hh}" if len(acima) else "-"
    print(f"{nome:17} {teto:7.2f} {trecho.max():6.2f}"
          f"   {quando}")
