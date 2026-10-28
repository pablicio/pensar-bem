entrada = "cento e vinte"

try:
    estoque = int(entrada)
except ValueError:
    print("valor inválido, usando zero")
    estoque = 0

print(estoque)
