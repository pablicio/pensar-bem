from pedido_da_cida import pedido_da_cida
from primeiro_modelo import FINANCEIRAS, primeiro_modelo
from risco.campeao import COLUNAS_FINAIS, treinado
from risco.dados import com_variaveis, tabela, treino_validacao

treino, _ = treino_validacao(tabela())
primeiro = primeiro_modelo(treino)
campeao = treinado()
cida = pedido_da_cida()

print("faturamento  atrasos  primeiro modelo  campeão")
for fat, atrasos in [(1830, 1), (2500, 1), (3000, 1),
                     (4200, 1), (4200, 0)]:
    outra = cida.copy()
    outra["faturamento_declarado"] = fat
    outra["atrasos_anteriores"] = atrasos
    outra = com_variaveis(outra)    # refaz o comprometimento
    p1 = primeiro.predict_proba(outra[FINANCEIRAS])[0, 1]
    p2 = campeao.predict_proba(outra[COLUNAS_FINAIS])[0, 1]
    print(f"{fat:11,} {atrasos:8} {p1:16.1%} {p2:8.1%}")
