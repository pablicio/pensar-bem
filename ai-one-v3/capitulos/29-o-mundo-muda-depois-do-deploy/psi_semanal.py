from em_producao import modelo, notas, pedidos, referencia
from risco.monitor import estado, psi

m = modelo()
ref = notas(m, referencia())
p = pedidos()
p["nota"] = notas(m, p)
semana = p["data_concessao"].dt.to_period("W").dt.start_time

print("semana pedidos ambulantes risco médio  PSI  situação")
for inicio, g in p.groupby(semana):
    festa = (g["tipo_negocio"] == "ambulante de festas").mean()
    valor = psi(ref, g["nota"])
    media = g["nota"].mean()
    print(f"{inicio:%d/%m} {len(g):7} {festa:10.0%}"
          f" {media:11.1%} {valor:5.2f}  {estado(valor)}")
