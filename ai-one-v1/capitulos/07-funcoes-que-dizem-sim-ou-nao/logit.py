import math

from sigmoide import sigmoide


def logit(p):
    return math.log(p / (1 - p))


a = (logit(0.9) - logit(0.5)) / (0.8 - 0.6)
b = logit(0.5) - a * 0.6
print(f"a = {a:.3f}  b = {b:.3f}")
print(f"conferindo: {sigmoide(a * 0.6 + b):.3f}"
      f" {sigmoide(a * 0.8 + b):.3f}")
