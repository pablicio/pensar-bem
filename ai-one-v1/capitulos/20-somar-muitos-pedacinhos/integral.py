def riemann(f, a, b, n):
    # n retângulos, com a altura tomada no começo de cada um
    largura = (b - a) / n
    total = 0
    for i in range(n):
        total += f(a + i * largura) * largura
    return total


def trapezio(f, a, b, n):
    largura = (b - a) / n
    total = 0
    for i in range(n):
        esquerda = f(a + i * largura)
        direita = f(a + (i + 1) * largura)
        total += (esquerda + direita) / 2 * largura
    return total
