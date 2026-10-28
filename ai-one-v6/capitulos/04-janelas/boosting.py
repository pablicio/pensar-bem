from sklearn.ensemble import HistGradientBoostingRegressor

from rio.avalia import erro_nos_picos, mae, parte
from rio.janelas import janelas
from rio.serie import nivel_cidade

nivel = nivel_cidade()
print("     MAE (cm)        erro médio nos picos (m)")
print(" h   persist. boost.  persist. boost.")
for h in (6, 12):
    x, y, _ = janelas(parte(nivel, "treino"), 24, h, passo=3)
    modelo = HistGradientBoostingRegressor(max_iter=200,
                                           random_state=0)
    modelo.fit(x, y)
    x, y, horas = janelas(parte(nivel, "teste"), 24, h)
    p = modelo.predict(x)
    pico_p = erro_nos_picos(nivel, 0 * p, horas, h)
    pico_b = erro_nos_picos(nivel, p, horas, h)
    print(f"{h:2d}   {mae(y) * 100:6.1f}"
          f" {mae(p - y) * 100:6.1f}"
          f"    {sum(pico_p) / len(pico_p):6.2f}"
          f" {sum(pico_b) / len(pico_b):6.2f}")
