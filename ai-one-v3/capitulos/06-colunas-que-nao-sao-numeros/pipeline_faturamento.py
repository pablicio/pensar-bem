from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from visitas import visitas

NUMERICAS = ["faturamento_declarado", "idade",
             "tempo_negocio_meses", "emprestimos_anteriores"]
CATEGORICAS = ["tipo_negocio", "regiao", "canal"]


def novo_modelo():
    prepara = ColumnTransformer([
        ("numeros", StandardScaler(), NUMERICAS),
        ("categorias", OneHotEncoder(handle_unknown="ignore"),
         CATEGORICAS),
    ])
    return Pipeline([("prepara", prepara),
                     ("regressao", LinearRegression())])


if __name__ == "__main__":
    t = visitas()
    X = t[NUMERICAS + CATEGORICAS]
    y = t["faturamento_verificado"]
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.25, random_state=42)
    modelo = novo_modelo().fit(X_treino, y_treino)
    previsto = modelo.predict(X_teste)
    erro = mean_absolute_error(y_teste, previsto)
    r2 = modelo.score(X_teste, y_teste)
    print(f"erro no teste: R$ {erro:,.2f}")
    print(f"R² no teste:   {r2:.3f}")
    nomes = modelo["prepara"].get_feature_names_out()
    print(f"{len(nomes)} colunas depois da preparação:")
    for nome in nomes[:6]:
        print("  ", nome)
    print("   ...")
