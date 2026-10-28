def normaliza_cpf(cpf):
    texto = str(cpf).strip()
    for sinal in ".- ":
        texto = texto.replace(sinal, "")
    return texto


assert normaliza_cpf("060.419.765-98") == "06041976598"
assert normaliza_cpf(6041976598) == "06041976598"
print("todas as conferências passaram")
