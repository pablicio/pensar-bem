import pandas as pd

from pipeline_faturamento import (CATEGORICAS, NUMERICAS,
                                  novo_modelo)
from visitas import visitas

t = visitas()
modelo = novo_modelo().fit(t[NUMERICAS + CATEGORICAS],
                           t["faturamento_verificado"])
novos = pd.DataFrame([
    {"faturamento_declarado": 3500, "idade": 31,
     "tempo_negocio_meses": 20, "emprestimos_anteriores": 0,
     "tipo_negocio": "técnico de celular",
     "regiao": "Cajazeiras", "canal": "feira"},
    {"faturamento_declarado": 3500, "idade": 31,
     "tempo_negocio_meses": 20, "emprestimos_anteriores": 0,
     "tipo_negocio": "tapioca", "regiao": "Cajazeiras",
     "canal": "feira"},
])
for i in range(len(novos)):
    previsto = modelo.predict(novos.iloc[[i]])[0]
    tipo = novos["tipo_negocio"].iloc[i]
    print(f"{tipo:20} R$ {previsto:,.2f}")

prepara = modelo["prepara"]
linha = prepara.transform(novos.iloc[[0]])
nomes = prepara.get_feature_names_out()
print()
print("o primeiro cliente, depois da preparação:")
for nome, valor in zip(nomes, linha.toarray()[0]):
    if valor != 0:
        print(f"  {nome:42} {valor:7.3f}")
