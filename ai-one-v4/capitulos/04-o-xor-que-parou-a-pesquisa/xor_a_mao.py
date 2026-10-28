def degrau(soma):
    return 1 if soma > 0 else 0


def rede(x1, x2):
    h1 = degrau(x1 + x2 - 0.5)       # OU: ao menos uma ligada
    h2 = degrau(x1 + x2 - 1.5)       # E: as duas ligadas
    saida = degrau(h1 - h2 - 0.5)    # OU, mas não E
    return h1, h2, saida


if __name__ == "__main__":
    print("x1 x2   h1 h2   saída")
    for x1 in (0, 1):
        for x2 in (0, 1):
            h1, h2, s = rede(x1, x2)
            print(f" {x1}  {x2}    {h1}  {h2}     {s}")
