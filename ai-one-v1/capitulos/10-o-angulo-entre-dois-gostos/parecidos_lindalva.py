import math

from clientes import ler_clientes
from distancias import distancia
from similaridade import cosseno

nomes, compras = ler_clientes("clientes.csv")
lindalva = compras[0]

print("cliente        distância  cosseno  ângulo")
for nome, v in zip(nomes[1:], compras[1:]):
    c = cosseno(lindalva, v)
    angulo = math.degrees(math.acos(min(c, 1.0)))
    d = distancia(lindalva, v)
    print(f"{nome:13s} {d:10.2f} {c:8.3f} {angulo:6.1f}°")
