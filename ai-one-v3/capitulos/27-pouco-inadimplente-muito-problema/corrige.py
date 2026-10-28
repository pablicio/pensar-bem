from precoce import divisao
from risco.modelos import COLUNAS, logistica

treino, valid = divisao()
modelo = logistica()
modelo.set_params(modelo__class_weight="balanced")
modelo.fit(treino[COLUNAS], treino["precoce"])
p = modelo.predict_proba(valid[COLUNAS])[:, 1]

# o peso multiplicou a chance por negativos/positivos; desfaz
pos = treino["precoce"].sum()
neg = len(treino) - pos
chance = p / (1 - p) * pos / neg
corrigida = chance / (1 + chance)
print(f"real na validação:   {valid['precoce'].mean():.1%}")
print(f"média com o peso:    {p.mean():.1%}")
print(f"média corrigida:     {corrigida.mean():.1%}")
