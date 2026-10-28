from pandas.api.types import is_numeric_dtype

from em_producao import pedidos, referencia
from risco.campeao import COLUNAS_FINAIS
from risco.monitor import estado, psi, psi_categorias

ref = referencia()
p = pedidos()
festa = p[p["data_concessao"] >= "2027-05-10"]

linhas = []
for c in COLUNAS_FINAIS:
    numero = is_numeric_dtype(ref[c]) and ref[c].dtype != bool
    if numero:
        valor = psi(ref[c], festa[c])
    else:
        valor = psi_categorias(ref[c], festa[c])
    linhas.append((valor, c))
print("coluna                   PSI  situação")
for valor, c in sorted(linhas, reverse=True):
    print(f"{c:22} {valor:5.2f}  {estado(valor)}")
