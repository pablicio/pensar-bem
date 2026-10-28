from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from risco.dados import tabela, treino_validacao

DUAS = ["idade", "comprometimento"]
treino, valid = treino_validacao(tabela())
amostra = treino.sample(3000, random_state=0)
print("    C   vetores   AUC")
for C in [0.01, 1, 100]:
    svm = SVC(kernel="rbf", gamma=0.1, C=C,
              class_weight="balanced")
    modelo = make_pipeline(StandardScaler(), svm)
    modelo.fit(amostra[DUAS], amostra["alvo"])
    auc = roc_auc_score(valid["alvo"],
                        modelo.decision_function(valid[DUAS]))
    print(f"{C:5} {svm.n_support_.sum():9,} {auc:5.3f}")
