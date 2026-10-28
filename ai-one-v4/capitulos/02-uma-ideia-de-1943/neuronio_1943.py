def neuronio(entradas, pesos, limiar):
    """O neurônio de 1943: dispara se a soma chega lá."""
    soma = sum(e * p for e, p in zip(entradas, pesos))
    return 1 if soma >= limiar else 0


print(" a  b   E  OU")
for a in (0, 1):
    for b in (0, 1):
        e = neuronio((a, b), (1, 1), limiar=2)
        ou = neuronio((a, b), (1, 1), limiar=1)
        print(f" {a}  {b}   {e}   {ou}")
print("NÃO 0 =", neuronio((0,), (-1,), limiar=0),
      " NÃO 1 =", neuronio((1,), (-1,), limiar=0))
