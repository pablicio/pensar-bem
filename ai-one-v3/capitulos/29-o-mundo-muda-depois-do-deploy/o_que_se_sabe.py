import pandas as pd

from em_producao import modelo, notas, pedidos

p = pedidos()
p["nota"] = notas(modelo(), p)
hoje = pd.Timestamp("2027-06-14")
p["vencidas"] = (hoje - p["data_concessao"]).dt.days // 30
p["em_atraso"] = p["dias_atraso_atual"] > 0
p["chegou_30"] = p["data_atraso_30"].notna()
festa = p["tipo_negocio"] == "ambulante de festas"
p["grupo"] = festa.map({True: "ambulante", False: "outros"})
mes = p["data_concessao"].dt.month.rename("mês")

resumo = p.groupby([mes, "grupo"]).agg(
    pedidos=("nota", "size"), vencidas=("vencidas", "median"),
    previsto=("nota", "mean"), atraso=("em_atraso", "mean"),
    a_30=("chegou_30", "mean"))
print(resumo.round(3).to_string())
