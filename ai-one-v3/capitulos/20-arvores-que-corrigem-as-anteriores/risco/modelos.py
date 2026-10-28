"""Os modelos de risco da Dendê, com a preparação junto."""
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.preprocessing import StandardScaler

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


def boosting(iteracoes=178):
    """Boosting de árvores rasas; categorias viram códigos."""
    codigos = OrdinalEncoder(
        handle_unknown="use_encoded_value",
        unknown_value=np.nan)
    prepara = ColumnTransformer(
        [("categorias", codigos, CATEGORICAS)],
        remainder="passthrough")
    modelo = HistGradientBoostingClassifier(
        learning_rate=0.05, max_iter=iteracoes, max_depth=2,
        min_samples_leaf=50, early_stopping=False,
        categorical_features=[0, 1, 2], random_state=0)
    return Pipeline([("prepara", prepara), ("modelo", modelo)])
