from clientes import ler_clientes
from distancias import distancia, norma
from operacoes import escalar
from similaridade import cosseno

nomes, compras = ler_clientes("clientes.csv")
lindalva = compras[0]
u = escalar(1 / norma(lindalva), lindalva)
for i in [1, 2]:
    v = escalar(1 / norma(compras[i]), compras[i])
    print(nomes[i], f"{distancia(u, v) ** 2:.4f}",
          f"{2 - 2 * cosseno(lindalva, compras[i]):.4f}")
