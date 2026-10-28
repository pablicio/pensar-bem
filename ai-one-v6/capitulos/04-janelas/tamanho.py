from sklearn.ensemble import HistGradientBoostingRegressor

from rio.avalia import erro_nos_picos, mae, parte
from rio.janelas import janelas
from rio.serie import nivel_cidade

nivel = nivel_cidade()
h = 12
print("janela  exemplos  MAE (cm)  erro nos picos (m)")
for passado in (6, 24, 72, 168, 240):
    treino = parte(nivel, "treino")
    x, y, _ = janelas(treino, passado, h, passo=3)
    modelo = HistGradientBoostingRegressor(max_iter=200,
                                           random_state=0)
    modelo.fit(x, y)
    xt, yt, horas = janelas(parte(nivel, "teste"), passado, h)
    p = modelo.predict(xt)
    picos = erro_nos_picos(nivel, p, horas, h)
    erro = mae(p - yt) * 100
    print(f"{passado:4d} h  {len(x):8d}  {erro:8.1f}"
          f"  {sum(picos) / len(picos):12.2f}")
