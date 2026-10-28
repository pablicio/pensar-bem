# Pedido 1.884, campanha VERAO10: 10% nos discos, frete inteiro
subtotal = 89.90 + 64.50 + 120.00
desconto = subtotal * 0.10
frete = 23.40
total = subtotal - desconto + frete

print(f"Subtotal: R$ {subtotal:.2f}")
print(f"Desconto: R$ {desconto:.2f}")
print(f"Frete:    R$ {frete:.2f}")
print(f"Total:    R$ {total:.2f}")
