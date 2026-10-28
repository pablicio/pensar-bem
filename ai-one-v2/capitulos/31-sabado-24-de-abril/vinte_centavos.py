from rateio.calculo import TARIFA
from rateio.reconciliacao import reconcilia

r = reconcilia("2027-02")
faltou = r["faltou"]
afetados = int((faltou > 0).sum())
maior = r["lado"].loc[faltou.idxmax(), "nome"]
print(f"cooperados com crédito a menos: {afetados:,}")
print(f"crédito que faltou: R$ {faltou.sum():,.2f}"
      f" ({r['faltou_kwh']:,.2f} kWh)")
print(f"maior perda: {maior}, R$ {faltou.max():,.2f}")
por_usina = faltou.groupby(r["lado"]["usina"]).sum()
print(por_usina.map("R$ {:,.2f}".format).to_string())
print(f"linha da sede na GED: R$ {r['sede_reais']:,.2f}"
      f" ({r['sede_kwh']:,.2f} kWh)")

diferenca = faltou.sum() - r["sede_reais"]
um_a_um = faltou.sum() - r["faltou_kwh"] * TARIFA
sobra = r["sobra_kwh"] * TARIFA
print(f"diferença: R$ {diferenca:.2f}")
print(f"  arredondamento dos reais, um a um: R$ {um_a_um:.2f}")
print(f"  sobra dos kWh do mês: {r['sobra_kwh']:.3f} kWh,"
      f" R$ {sobra:.2f}")
