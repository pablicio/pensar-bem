import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from atrasos import PERFIL, atrasados

t = atrasados()
modelo = make_pipeline(StandardScaler(),
                       KMeans(4, n_init=10, random_state=0))
t["grupo"] = modelo.fit_predict(t[PERFIL])

print("empréstimos por grupo:", t["grupo"].value_counts()
      .sort_index().tolist())
perfil = t.groupby("grupo")[PERFIL + ["chegou_a_90"]].mean()
pd.set_option("display.float_format", "{:,.2f}".format)
print(perfil.T)
