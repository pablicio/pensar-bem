original = [{"nome": "Tomate"}, {"nome": "Alface"}]
copia = original[:]

copia[0]["nome"] = "Beterraba"
print(original[0]["nome"])   # Beterraba
