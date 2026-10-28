def segredo(nome: str) -> str:
    caminho = os.environ.get(f"{nome}_FILE")
    if caminho:
        with open(caminho) as f:
            return f.read().strip()
    return os.environ[nome]

SENHA_BANCO = segredo("SENHA_BANCO")
