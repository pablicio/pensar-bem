from mnist import carregar

imagens, rotulos = carregar("treino")
print(f"{len(imagens):,} imagens; a primeira é {rotulos[0]}")
TONS = " .:-=+*#%@"            # do papel à tinta mais escura
for linha in imagens[0]:
    texto = "".join(TONS[int(v) * 10 // 256] for v in linha)
    if texto.strip():          # pula as linhas em branco
        print(texto.rstrip())
