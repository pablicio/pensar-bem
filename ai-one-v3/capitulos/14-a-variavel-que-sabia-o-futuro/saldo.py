from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from risco.dados import tabela, treino_validacao
from risco.modelos import CATEGORICAS, NUMERICAS

numeros = NUMERICAS + ["saldo_devedor"]
prepara = ColumnTransformer([
    ("numeros", StandardScaler(), numeros),
    ("categorias", OneHotEncoder(handle_unknown="ignore"),
     CATEGORICAS)])
modelo = Pipeline([("prepara", prepara),
                   ("modelo", LogisticRegression(
                       max_iter=5_000))])
treino, valid = treino_validacao(tabela())
colunas = numeros + CATEGORICAS
modelo.fit(treino[colunas], treino["alvo"])
p = modelo.predict_proba(valid[colunas])[:, 1]
auc = roc_auc_score(valid["alvo"], p)
print(f"com saldo_devedor: AUC {auc:.3f}")
