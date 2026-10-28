import matplotlib.pyplot as plt
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from risco.dados import tabela, treino_validacao

DUAS = ["idade", "comprometimento"]

treino, _ = treino_validacao(tabela())
amostra = treino.sample(3000, random_state=0)
idade = np.linspace(20, 75, 200)
comp = np.linspace(0, 0.8, 200)
I, C = np.meshgrid(idade, comp)
grade = np.column_stack([I.ravel(), C.ravel()])
pontos = amostra.sample(400, random_state=1)

fig, eixos = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
for ax, kernel in zip(eixos, ["linear", "rbf"]):
    svm = SVC(kernel=kernel, gamma=2, class_weight="balanced")
    modelo = make_pipeline(StandardScaler(), svm)
    modelo.fit(amostra[DUAS].to_numpy(), amostra["alvo"])
    nota = modelo.decision_function(grade).reshape(I.shape)
    ax.contourf(I, C, nota > 0, alpha=0.25, cmap="coolwarm")
    ax.scatter(pontos["idade"], pontos["comprometimento"],
               c=pontos["alvo"], cmap="coolwarm", s=8)
    ax.set_ylim(0, 0.8)
    ax.set_title(f"kernel {kernel}")
    ax.set_xlabel("idade")
eixos[0].set_ylabel("comprometimento declarado")
fig.tight_layout()
fig.savefig("fronteiras.png", dpi=300)
