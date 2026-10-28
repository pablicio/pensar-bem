from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from risco.dados import tabela, treino_validacao

DUAS = ["idade", "comprometimento"]
treino, valid = treino_validacao(tabela())
amostra = treino.sample(3000, random_state=0)
modelos = {
    "logística": LogisticRegression(),
    "SVM linear": SVC(kernel="linear",
                      class_weight="balanced"),
    "SVM RBF, gama 0,1": SVC(kernel="rbf", gamma=0.1,
                             class_weight="balanced"),
    "SVM RBF, gama 2": SVC(kernel="rbf", gamma=2,
                           class_weight="balanced"),
}
print("modelo              AUC  vetores de suporte")
for nome, svm in modelos.items():
    modelo = make_pipeline(StandardScaler(), svm)
    modelo.fit(amostra[DUAS], amostra["alvo"])
    nota = modelo.decision_function(valid[DUAS])
    auc = roc_auc_score(valid["alvo"], nota)
    vetores = getattr(svm, "n_support_", None)
    texto = "" if vetores is None else f"{vetores.sum():,}"
    print(f"{nome:18} {auc:.3f} {texto:>19}")
