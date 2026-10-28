from rio.avalia import mae
from rio.serie import ler

# um trecho de hora em hora, depois da régua nova
leitura = ler("cadernos")["leitura_cm"].loc["1996-07":"2002"]
real = (leitura[leitura < 1400] / 100).asfreq("h")
# finge que só houve leituras de três em três horas
de_tres = real.where(real.index.hour % 3 == 0)
interpolada = de_tres.interpolate(limit_area="inside")
erro = (interpolada - real)[real.index.hour % 3 != 0]
print(f"erro médio da interpolação: {mae(erro) * 100:.2f} cm")
print(f"maior erro: {erro.abs().max() * 100:.0f} cm,"
      f" em {erro.abs().idxmax():%d/%m/%Y %Hh}")
subindo = real.diff().abs() > 0.2
rapidas = mae(erro[subindo]) * 100
print(f"nas subidas rápidas: {rapidas:.1f} cm")
