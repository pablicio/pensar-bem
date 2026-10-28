precos = [8.90, 3.50, 12.00, 5.25]

total = 0.0
caros = 0

for preco in precos:
    total += preco
    if preco > 10:
        caros += 1

print(f"total R$ {total:.2f}, {caros} acima de 10")
