from distribuicoes import poisson

lam = 1.3 * 1140 * 0.007
uma_hora = 1 - sum(poisson(k, lam) for k in range(13))
print(f"média {lam:.1f}; uma hora acima de 12: {uma_hora:.3f}")
alguma = 1 - (1 - uma_hora) ** 4
print(f"alguma das quatro horas: {alguma:.3f}")
