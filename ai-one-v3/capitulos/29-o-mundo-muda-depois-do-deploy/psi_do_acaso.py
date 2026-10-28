import numpy as np

from em_producao import modelo, notas, referencia
from risco.monitor import psi

ref = notas(modelo(), referencia())
sorteio = np.random.default_rng(0)
# semanas de mentira: 225 pedidos sorteados do próprio treino
valores = [psi(ref, sorteio.choice(ref, 225, replace=False))
           for _ in range(500)]
for q in [50, 90, 99]:
    print(f"percentil {q}: {np.percentile(valores, q):.3f}")
