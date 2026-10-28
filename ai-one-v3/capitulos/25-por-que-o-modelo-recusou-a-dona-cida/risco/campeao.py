"""O modelo escolhido no capítulo 21, pronto para usar."""
from risco.dados import lacrar, tabela
from risco.finalidade import com_divida
from risco.modelos import COLUNAS, boosting

COLUNAS_FINAIS = COLUNAS + ["divida"]
BOTOES = {"learning_rate": 0.112, "max_iter": 325,
          "max_depth": 1, "min_samples_leaf": 74,
          "l2_regularization": 0.0225}


def campeao():
    """O boosting com os botões da busca, ainda sem treino."""
    botoes = {f"modelo__{k}": v for k, v in BOTOES.items()}
    return boosting().set_params(**botoes)


def treinado():
    """Treina o campeão em tudo o que não está lacrado."""
    aberto, _ = lacrar(com_divida(tabela()))
    modelo = campeao()
    modelo.fit(aberto[COLUNAS_FINAIS], aberto["alvo"])
    return modelo
