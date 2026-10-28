import random


def acervo_do_ivo(semente):
    # o valor de revenda, em reais, de cada um dos 4.200 discos
    random.seed(semente)
    discos = []
    for _ in range(4200):
        sorte = random.random()
        if sorte < 0.55:
            valor = random.randint(5, 25)      # comum
        elif sorte < 0.90:
            valor = random.randint(25, 70)     # procurado
        elif sorte < 0.995:
            valor = random.randint(70, 290)    # raro
        else:
            valor = random.randint(300, 2500)  # raríssimo
        discos.append(valor)
    return discos
