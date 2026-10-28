from duas_alavancas import gradiente, lucro


def perda(preco, centenas):
    return -lucro(preco, 100 * centenas) / 100


p, c = 89.90, 0.0
for passo in range(1, 101):
    gp, gc = gradiente(perda, p, c)
    p, c = p - 4 * gp, c - 4 * gc
    if passo in [1, 2, 5, 20, 100]:
        print(f"passo {passo:3d}: R$ {p:6.2f},"
              f" anúncio R$ {100 * c:6.1f}")
