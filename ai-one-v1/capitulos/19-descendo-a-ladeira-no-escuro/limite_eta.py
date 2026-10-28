for eta in [0.19, 0.21]:
    x = 0.0
    for _ in range(50):
        x = x - eta * 10 * (x - 3)
    print(eta, round(x, 4))
