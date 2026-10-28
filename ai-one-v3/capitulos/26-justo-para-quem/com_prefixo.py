import pandas as pd
from sklearn.metrics import roc_auc_score

from por_regiao import por_regiao
from regioes import divisao
from risco.campeao import COLUNAS_FINAIS, campeao

treino, valid = divisao()
lado = {}
for nome, colunas in [("sem", COLUNAS_FINAIS),
                      ("com", COLUNAS_FINAIS + ["prefixo"])]:
    modelo = campeao().fit(treino[colunas], treino["alvo"])
    nota = modelo.predict_proba(valid[colunas])[:, 1]
    auc = roc_auc_score(valid["alvo"], nota)
    print(f"{nome} o prefixo: AUC {auc:.4f}")
    lado[nome] = por_regiao(valid, nota)["aprova"]

aprova = pd.DataFrame(lado).sort_values("sem")
print("\naprovação por região")
print(aprova.round(3).to_string())
dif = aprova.max() - aprova.min()
print(f"\ndistância entre a maior e a menor: "
      f"{dif['sem']:.1%} sem, {dif['com']:.1%} com")
