from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier

from regra_jussara import regras_da_jussara
from risco.dados import tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, valid = treino_validacao(tabela())
arvore = DecisionTreeClassifier(min_samples_leaf=200,
                                random_state=0)
arvore.fit(treino[NUMERICAS], treino["alvo"])
nota = arvore.predict_proba(valid[NUMERICAS])[:, 1]
auc = roc_auc_score(valid["alvo"], nota)
print(f"folhas: {arvore.get_n_leaves()}, AUC: {auc:.3f}")


def aprova_os_melhores(fracao):
    """Aprova a fração de menor risco segundo a árvore."""
    return nota.argsort().argsort() < fracao * len(nota)


alvo = valid["alvo"].to_numpy()
regra = regras_da_jussara(valid).all(axis=1).to_numpy()
print()
print("                  aprova  chegam a 90 dias")
mesma = aprova_os_melhores(regra.mean())
for nome, aprova in [("regra da Jussara", regra),
                     ("árvore", mesma),
                     ("árvore", aprova_os_melhores(0.60))]:
    taxa = alvo[aprova].mean()
    print(f"{nome:16} {aprova.mean():8.0%} {taxa:17.1%}")

comum = (regra & mesma).sum()
print(f"\naprovados pelas duas: {comum:,} de {regra.sum():,}")
