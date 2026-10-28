"""O alvo: chegar a 90 dias de atraso em até 12 meses."""
import pandas as pd

EXTRATO = pd.Timestamp("2027-03-12")   # o dia da extração
JANELA = 365                          # dias após a concessão

# o que se sabe no dia da concessão
PEDIDO = ["produto", "valor", "parcelas", "finalidade",
          "tipo_negocio", "canal", "idade",
          "tempo_negocio_meses", "cliente_desde_meses",
          "emprestimos_anteriores", "atrasos_anteriores",
          "faturamento_declarado", "telefone_referencia",
          "agente"]
DATAS = ["data_atraso_30", "data_atraso_60", "data_atraso_90",
         "data_quitacao", "data_baixa"]


def carteira():
    """Os empréstimos com o que a cobrança sabe de cada um."""
    emp = pd.read_csv("dados/brutos/emprestimos.csv",
                      parse_dates=["data_concessao"])
    cob = pd.read_csv("dados/brutos/cobranca.csv",
                      parse_dates=DATAS)
    return emp.merge(cob, on="pedido_id",
                     validate="one_to_one")


def maduros(t):
    """Os empréstimos com a janela inteira já observada."""
    limite = EXTRATO - pd.Timedelta(days=JANELA)
    return t[t["data_concessao"] <= limite].copy()


def com_alvo(t):
    """Os maduros, com a coluna alvo: 1 se chegou a 90 dias."""
    t = maduros(t)
    prazo = (t["data_atraso_90"] - t["data_concessao"]).dt.days
    t["alvo"] = (prazo <= JANELA).astype(int)
    return t
