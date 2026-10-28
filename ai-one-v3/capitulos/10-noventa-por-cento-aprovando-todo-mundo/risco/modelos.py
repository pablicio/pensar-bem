"""Os modelos de risco da Dendê, com a preparação junto."""
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERICAS = ["valor", "parcelas", "faturamento_declarado",
             "comprometimento", "atrasos_anteriores", "idade",
             "tempo_negocio_meses", "cliente_desde_meses",
             "emprestimos_anteriores"]
CATEGORICAS = ["produto", "tipo_negocio", "canal"]
COLUNAS = NUMERICAS + CATEGORICAS


def preparacao():
    return ColumnTransformer([
        ("numeros", StandardScaler(), NUMERICAS),
        ("categorias", OneHotEncoder(handle_unknown="ignore"),
         CATEGORICAS)])


def logistica():
    """A regressão logística com o histórico do cliente."""
    return Pipeline([
        ("prepara", preparacao()),
        ("modelo", LogisticRegression(max_iter=5_000))])
