def conta(x, w, b):
    a = w * x          # nó ×: multiplicação
    s = a + b          # nó +: soma
    L = s ** 2         # nó ²: quadrado
    return a, s, L


x, w, b = 2.0, 0.5, -3.0

# para frente: os valores
a, s, L = conta(x, w, b)
print(f"para frente: a = {a}, s = {s}, L = {L}")

# para trás: cada nó multiplica o que chega pela derivada local
dL = 1.0                    # dL/dL
ds = dL * 2 * s             # d(s²)/ds = 2s
da = ds * 1.0               # d(a + b)/da = 1
db = ds * 1.0               # d(a + b)/db = 1
dw = da * x                 # d(w x)/dw = x
dx = da * w                 # d(w x)/dx = w
print(f"para trás: dL/ds = {ds}, dL/da = {da}")
print(f"           dL/dw = {dw}, dL/dx = {dx}, dL/db = {db}")


def numerica(f, v, h=1e-6):
    """A derivada numérica central de f no ponto v."""
    return (f(v + h) - f(v - h)) / (2 * h)


nw = numerica(lambda v: conta(x, v, b)[2], w)
nx = numerica(lambda v: conta(v, w, b)[2], x)
nb = numerica(lambda v: conta(x, w, v)[2], b)
print(f"numéricas: dL/dw = {nw:.6f}, dL/dx = {nx:.6f},"
      f" dL/db = {nb:.6f}")
