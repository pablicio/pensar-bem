p = 0.004
sens = 0.95
falso = 0.02
while sens * p / (sens * p + falso * (1 - p)) < 0.5:
    falso = falso * 0.99
print(f"falso alarme necessário: {falso:.5f}")
nova = sens * p / (sens * p + 0.005 * (1 - p))
print(f"com 0,5%: {nova:.3f}")
