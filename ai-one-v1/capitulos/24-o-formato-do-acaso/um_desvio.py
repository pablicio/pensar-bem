from distribuicoes import normal
from gerar_balcao import vendas_do_mes
from integral import trapezio
from resumo import desvio_padrao, media

totais = [sum(vendas_do_mes(dia, 30)) for dia in range(2000)]
m, s = media(totais), desvio_padrao(totais)
dentro = sum(1 for t in totais if abs(t - m) < s) / len(totais)
esperado = trapezio(lambda x: normal(x, m, s),
                    m - s, m + s, 1000)
print(f"simulação: {dentro:.3f}  normal: {esperado:.3f}")
