from gerar_balcao import vendas_do_mes
from resumo import desvio_padrao, media

comuns = vendas_do_mes(1225, 115)
m, s = media(comuns), desvio_padrao(comuns)
z = [(x - m) / s for x in comuns]
print(f"média {media(z):.6f}, desvio {desvio_padrao(z):.6f}")
acima = sum(1 for valor in z if abs(valor) > 2)
print("acima de 2 desvios:", acima)
