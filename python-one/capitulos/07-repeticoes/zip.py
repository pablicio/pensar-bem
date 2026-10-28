nomes = ["Tomate", "Alface"]
precos = [8.90, 3.50]

for nome, preco in zip(nomes, precos):
    print(f"{nome}: R$ {preco:.2f}")
