import math

taxa_ano = (9000 / 2400) ** (1 / 7) - 1
taxa_mes = (1 + taxa_ano) ** (1 / 12) - 1
meses = math.log(2) / math.log(1 + taxa_mes)
print(f"meses exatos: {meses:.2f}")
print(f"primeiro mês inteiro: {math.ceil(meses)}")
