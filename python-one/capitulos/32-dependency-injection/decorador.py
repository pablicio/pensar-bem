def registrar(funcao):
    def dentro(*args, **kwargs):
        print(f"chamando {funcao.__name__}")
        return funcao(*args, **kwargs)
    return dentro


@registrar
def somar(a, b):
    return a + b


print(somar(2, 3))
