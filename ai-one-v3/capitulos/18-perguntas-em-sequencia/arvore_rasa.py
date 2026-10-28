from sklearn.tree import DecisionTreeClassifier, export_text

from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, _ = treino_validacao(tabela())
arvore = DecisionTreeClassifier(max_depth=3, random_state=0)
arvore.fit(treino[NUMERICAS], treino["alvo"])
print(export_text(arvore, feature_names=NUMERICAS,
                  show_weights=True, decimals=2))
