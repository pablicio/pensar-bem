"""Os botões do boosting e as faixas onde procurar."""
from scipy.stats import loguniform, randint

from risco.modelos import COLUNAS

COL = COLUNAS + ["divida"]
BOTOES = {"modelo__learning_rate": loguniform(0.005, 0.5),
          "modelo__max_iter": randint(20, 1_000),
          "modelo__max_depth": randint(1, 7),
          "modelo__min_samples_leaf": randint(5, 300),
          "modelo__l2_regularization": loguniform(1e-3, 10)}
