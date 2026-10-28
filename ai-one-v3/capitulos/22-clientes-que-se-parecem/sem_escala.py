from sklearn.cluster import KMeans

from atrasos import PERFIL, atrasados

t = atrasados()
km = KMeans(4, n_init=10, random_state=0).fit(t[PERFIL])
t["grupo"] = km.labels_
curtos = {"valor": "valor",
          "faturamento_declarado": "faturamento",
          "idade": "idade", "atrasos_anteriores": "atrasos",
          "chegou_a_90": "chegou_a_90"}
medias = t.groupby("grupo")[list(curtos)].mean().round(2)
print(medias.rename(columns=curtos).to_string())
