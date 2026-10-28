try:
    arquivo = abrir(caminho)
except OSError as erro:
    print(f"não consegui abrir: {erro}")
else:
    processar(arquivo)
finally:
    limpar_temporarios()
