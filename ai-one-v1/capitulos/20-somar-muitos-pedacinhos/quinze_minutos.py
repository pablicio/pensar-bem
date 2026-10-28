from integral import riemann, trapezio
from promocao import vendas_por_hora

r = riemann(vendas_por_hora, 0, 20, 80)
t = trapezio(vendas_por_hora, 0, 20, 80)
print(f"retângulos: R$ {r:.2f} (erro de R$ {15000 - r:.2f})")
print(f"trapézios:  R$ {t:.2f} (erro de R$ {15000 - t:.2f})")
