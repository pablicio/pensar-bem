from rio.serie import nivel_cidade

nivel = nivel_cidade()
print(len(nivel), "horas, de", nivel.index[0])
print("a", nivel.index[-1])
print("horas sem nível:", int(nivel.isna().sum()))
print(f"máximo: {nivel.max():.2f} m"
      f" em {nivel.idxmax():%d/%m/%Y %Hh}")
for ano in ("1983", "1984", "2008", "2023"):
    print(ano, f"{nivel.loc[ano].max():.2f} m")
