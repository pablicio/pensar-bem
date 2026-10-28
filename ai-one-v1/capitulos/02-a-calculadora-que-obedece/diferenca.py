planilha = 89.90 + 64.50 + 120.00 * 0.9 + 23.40
correto = (89.90 + 64.50 + 120.00) * 0.9 + 23.40
diferenca = planilha - correto
pelos_discos = (89.90 + 64.50) * 0.10
print(f"Diferença pelos totais: R$ {diferenca:.2f}")
print(f"Desconto que faltou:    R$ {pelos_discos:.2f}")
