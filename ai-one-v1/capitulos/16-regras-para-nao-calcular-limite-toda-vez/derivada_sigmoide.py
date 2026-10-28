from sigmoide import sigmoide

for z in range(-4, 5):
    s = sigmoide(z)
    print(f"{z:2d}  {s * (1 - s):.4f}")
