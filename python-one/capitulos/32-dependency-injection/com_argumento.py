def repetir(vezes):
    def decorador(funcao):
        def dentro(*args, **kwargs):
            for _ in range(vezes):
                resultado = funcao(*args, **kwargs)
            return resultado
        return dentro
    return decorador


@repetir(3)
def avisar():
    print("oi")
