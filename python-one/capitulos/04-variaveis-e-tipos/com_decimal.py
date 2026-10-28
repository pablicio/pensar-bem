from decimal import Decimal

total = Decimal("0.00")
for _ in range(1000):
    total += Decimal("8.90")

print(total)
