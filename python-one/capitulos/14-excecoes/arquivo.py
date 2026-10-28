with open("catalogo.csv", encoding="utf-8") as f:
    for linha in f:
        print(linha.strip())
