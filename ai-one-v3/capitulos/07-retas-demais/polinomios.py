from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import (OneHotEncoder,
                                   PolynomialFeatures,
                                   StandardScaler)

from pipeline_faturamento import CATEGORICAS, NUMERICAS
from visitas import visitas


def modelo_polinomial(grau):
    """A regressão do capítulo 6, com termos até o grau."""
    numeros = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(grau, include_bias=False),
        StandardScaler())
    prepara = ColumnTransformer([
        ("numeros", numeros, NUMERICAS),
        ("categorias", OneHotEncoder(handle_unknown="ignore"),
         CATEGORICAS)])
    return Pipeline([("prepara", prepara),
                     ("regressao", LinearRegression())])


def tres_partes():
    """Treino, validação e teste; o teste fica guardado."""
    t = visitas()
    X = t[NUMERICAS + CATEGORICAS]
    y = t["faturamento_verificado"]
    X_resto, X_teste, y_resto, y_teste = train_test_split(
        X, y, test_size=0.25, random_state=42)
    X_treino, X_valid, y_treino, y_valid = train_test_split(
        X_resto, y_resto, test_size=0.25, random_state=7)
    return X_treino, X_valid, y_treino, y_valid
