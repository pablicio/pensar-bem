import numpy as np

from perdas import entropia_cruzada, quadratica, softmax

# saídas de uma rede para um dígito que é um 3 (dez classes)
casos = {"certa e segura": 8.0, "certa, em dúvida": 1.0,
         "errada, em dúvida": -1.0, "errada e segura": -8.0}
print("caso                p(3)  quadrática  entropia cruzada")
for nome, nota in casos.items():
    z = np.zeros(10)
    z[3] = nota
    p3 = softmax(z)[3]
    print(f"{nome:18} {p3:5.3f} {quadratica(z, 3):11.3f}"
          f" {entropia_cruzada(z, 3):17.3f}")
