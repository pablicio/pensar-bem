from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from risco.modelos import CATEGORICAS, NUMERICAS

COM_ATRASO = NUMERICAS + ["dias_atraso_atual"]


def logistica_com_atraso():
    """A logística do capítulo 10, mais a coluna suspeita."""
    prepara = ColumnTransformer([
        ("numeros", StandardScaler(), COM_ATRASO),
        ("categorias", OneHotEncoder(handle_unknown="ignore"),
         CATEGORICAS)])
    logistica = LogisticRegression(max_iter=5_000)
    return Pipeline([("prepara", prepara),
                     ("modelo", logistica)])
