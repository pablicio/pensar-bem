"""Os empréstimos que chegaram a 30 dias de atraso."""
import pandas as pd

from risco.alvo import EXTRATO, carteira
from risco.dados import com_variaveis

PERFIL = ["valor", "parcelas", "faturamento_declarado",
          "comprometimento", "idade", "tempo_negocio_meses",
          "cliente_desde_meses", "emprestimos_anteriores",
          "atrasos_anteriores", "parcela_do_atraso"]


def atrasados():
    """Os que chegaram a 30 dias a tempo de se saber o fim."""
    t = com_variaveis(carteira())
    limite = EXTRATO - pd.Timedelta(days=60)
    t = t[t["data_atraso_30"] <= limite].copy()
    dias = (t["data_atraso_30"] - t["data_concessao"]).dt.days
    # a parcela que deixou de ser paga: 30 dias antes do marco
    t["parcela_do_atraso"] = (dias - 30) // 30
    t["chegou_a_90"] = t["data_atraso_90"].notna()
    return t
