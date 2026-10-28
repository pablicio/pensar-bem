from duas_alavancas import lucro

melhor = (0, 0, 0)
for i in range(121):
    p = 60 + 0.5 * i
    for a in range(0, 2001, 5):
        valor = lucro(p, a)
        if valor > melhor[0]:
            melhor = (valor, p, a)
print(f"preço R$ {melhor[1]:.2f}, anúncio R$ {melhor[2]}, "
      f"lucro R$ {melhor[0]:.2f}")
