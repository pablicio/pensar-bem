def reta_por_dois_pontos(x1, y1, x2, y2):
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b


a, b = reta_por_dois_pontos(6, 58, 9, 104)
print(f"a = {a:.2f}  b = {b:.2f}")
print(f"nota 7: R$ {a * 7 + b:.2f}")
a, b = reta_por_dois_pontos(5, 45, 10, 120)
print(f"a = {a:.2f}  b = {b:.2f}")
