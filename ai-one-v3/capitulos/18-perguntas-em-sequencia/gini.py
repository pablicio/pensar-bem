from risco.dados import tabela, treino_validacao


def gini(y):
    """A chance de errar sorteando o rótulo pela proporção."""
    p = y.mean()
    return 1 - p**2 - (1 - p) ** 2


def depois_da_pergunta(t, limite):
    """A impureza média dos dois lados, pesada pelo tamanho."""
    sim = t["comprometimento"] <= limite
    lados = [t.loc[sim, "alvo"], t.loc[~sim, "alvo"]]
    return sum(len(l) / len(t) * gini(l) for l in lados)


treino, _ = treino_validacao(tabela())
print(f"antes de perguntar:      {gini(treino['alvo']):.4f}")
for limite in [0.30, 0.37]:
    g = depois_da_pergunta(treino, limite)
    print(f"comprometimento <= {limite:.2f}: {g:.4f}")
