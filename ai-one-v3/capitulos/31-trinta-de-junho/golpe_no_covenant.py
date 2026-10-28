import pandas as pd

from concedidos import concedidos

emp = pd.read_csv("dados/brutos/emprestimos.csv")
junho = pd.read_csv("dados/brutos/fechamento_cobranca.csv")
junho = junho.merge(concedidos(), on="pedido_id")
ativa = junho[junho["situacao"].isin(["em dia", "atraso"])]
ruim = ativa[ativa["dias_atraso_atual"] > 90]

fone = emp["telefone_referencia"] == "(71) 98877-1203"
nove = emp.loc[fone, "pedido_id"]
do_golpe = ruim[ruim["pedido_id"].isin(nove)]
golpe = do_golpe["saldo_devedor"].sum()
sem = ruim["saldo_devedor"].sum() - golpe
print(f"saldo ruim do golpe: R$ {golpe:,.0f}"
      f" em {len(do_golpe)} empréstimos")
print(f"inadimplência sem o golpe: "
      f"{sem / ativa['saldo_devedor'].sum():.2%}")
