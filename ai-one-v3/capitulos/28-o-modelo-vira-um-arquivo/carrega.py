import numpy as np
import skops.io as sio

from pedido_da_cida import pedido_da_cida
from risco.campeao import COLUNAS_FINAIS, treinado
from risco.dados import lacrar, tabela
from risco.finalidade import com_divida

arquivo = "modelos/campeao-1.0.0.skops"
desconhecidos = sio.get_untrusted_types(file=arquivo)
print("tipos que o skops não conhece de antemão:")
for tipo in desconhecidos:
    print("  ", tipo)

# depois de ler a lista e concordar com ela:
modelo = sio.load(arquivo, trusted=desconhecidos)
cida = pedido_da_cida()[COLUNAS_FINAIS]
print(f"\nDona Cida pelo arquivo: "
      f"{modelo.predict_proba(cida)[0, 1]:.1%}")

aberto, _ = lacrar(com_divida(tabela()))
X = aberto[COLUNAS_FINAIS]
iguais = np.array_equal(modelo.predict_proba(X),
                        treinado().predict_proba(X))
print("mesmas notas que o modelo recém-treinado:", iguais)
