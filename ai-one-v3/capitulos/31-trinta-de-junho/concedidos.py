"""O que de fato foi emprestado até 11 de junho."""
import pandas as pd

from em_producao import modelo, notas, pedidos

DEPLOY = pd.Timestamp("2027-05-17")
CORTE = 0.13                  # o da reunião com o banco


def concedidos(com_modelo=True):
    """O extrato inteiro, mais os aprovados em produção."""
    emp = pd.read_csv("dados/brutos/emprestimos.csv",
                      parse_dates=["data_concessao"])
    p = pedidos()
    aprova = pd.Series(True, index=p.index)
    if com_modelo:
        nota = notas(modelo(), p)
        festa = p["tipo_negocio"] == "ambulante de festas"
        regra_12 = ~(festa & (p["valor"] > 1500))
        decide = (nota < CORTE) & regra_12
        aprova = (p["data_concessao"] < DEPLOY) | decide
    colunas = ["pedido_id", "data_concessao", "valor"]
    return pd.concat([emp[colunas], p.loc[aprova, colunas]])


def covenant(cobranca):
    """Saldo com mais de 90 dias de atraso / saldo total."""
    ativa = cobranca[cobranca["situacao"].isin(["em dia",
                                                "atraso"])]
    ruim = ativa["dias_atraso_atual"] > 90
    return (ativa.loc[ruim, "saldo_devedor"].sum()
            / ativa["saldo_devedor"].sum())
