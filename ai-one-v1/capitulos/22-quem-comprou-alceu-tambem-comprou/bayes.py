import random

p_fraude = 0.004        # taxa de base: 4 em mil pedidos
sensibilidade = 0.95    # P(alerta | fraude), do slide 31
falso_alarme = 0.02     # P(alerta | honesto), do slide 31

p_alerta = (sensibilidade * p_fraude
            + falso_alarme * (1 - p_fraude))
p_fraude_dado_alerta = sensibilidade * p_fraude / p_alerta
print(f"P(alerta)          = {p_alerta:.5f}")
print(f"P(fraude | alerta) = {p_fraude_dado_alerta:.4f}")

random.seed(12)
alertas = 0
fraudes_alertadas = 0
for _ in range(200_000):
    fraude = random.random() < p_fraude
    chance = sensibilidade if fraude else falso_alarme
    if random.random() < chance:
        alertas += 1
        if fraude:
            fraudes_alertadas += 1
print(f"simulação: {alertas} alertas, "
      f"{fraudes_alertadas} fraudes, "
      f"{fraudes_alertadas / alertas:.4f}")
