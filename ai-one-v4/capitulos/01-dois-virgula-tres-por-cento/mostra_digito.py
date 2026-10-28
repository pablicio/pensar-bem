import numpy as np

from mnist import carregar

imagens, rotulos = carregar("teste")
imagem = imagens[0]
print(f"rótulo: {rotulos[0]}; formato: {imagem.shape}")
TONS = " .:-=+*#%@"
for linha in imagem:
    texto = "".join(TONS[int(v) * 10 // 256] for v in linha)
    if texto.strip():
        print(texto.rstrip())

vetor = imagem.reshape(784)    # as linhas, uma depois da outra
print(f"\nvetor: formato {vetor.shape},"
      f" de {vetor.min()} a {vetor.max()}")
print(f"pixels com tinta: {np.count_nonzero(vetor)} de 784")
print("a linha 10 da imagem é o trecho 280 a 307 do vetor:")
np.set_printoptions(linewidth=60)
print(vetor[280:308])
