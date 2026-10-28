"""Pontos no plano: dentro do círculo é +1, fora é −1."""
import random


def pontos(n=100, semente=0):
    r = random.Random(semente)
    xs, ys = [], []
    for _ in range(n):
        x = [r.uniform(-1, 1), r.uniform(-1, 1)]
        dentro = x[0] ** 2 + x[1] ** 2 < 0.5
        xs.append(x)
        ys.append(1.0 if dentro else -1.0)
    return xs, ys
