from sklearn.ensemble import HistGradientBoostingRegressor

from rio.avalia import erro_nos_picos, mae, parte
from rio.entradas import NIVEIS, tabela
from rio.janelas import janelas_tabela

tab = tabela()
nivel = tab["cidade"]
print(" h   entradas        MAE (cm)   picos (m)")
for h in (6, 12):
    tudo = list(tab.columns)
    for nome, colunas in (("só a cidade", ["cidade"]),
                          ("a bacia inteira", tudo)):
        dados = tab[colunas]
        x, y, _ = janelas_tabela(parte(dados, "treino"),
                                 parte(nivel, "treino"), 24, h,
                                 passo=3)
        xt, yt, horas = janelas_tabela(parte(dados, "teste"),
                                       parte(nivel, "teste"),
                                       24, h)
        # os níveis, relativos à última hora da janela
        for j, coluna in enumerate(colunas):
            if coluna in NIVEIS:
                x[:, :, j] -= x[:, -1:, j]
                xt[:, :, j] -= xt[:, -1:, j]
        m = HistGradientBoostingRegressor(max_iter=200,
                                          random_state=0)
        m.fit(x.reshape(len(x), -1), y)
        p = m.predict(xt.reshape(len(xt), -1))
        picos = erro_nos_picos(nivel, p, horas, h)
        print(f"{h:2d}   {nome:15} {mae(p - yt) * 100:8.1f}"
              f" {sum(picos) / len(picos):11.2f}")
