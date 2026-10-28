from pwdlib import PasswordHash

hasher = PasswordHash.recommended()


def gerar_hash(senha: str) -> str:
    return hasher.hash(senha)


def conferir_senha(senha: str, hash_guardado: str) -> bool:
    return hasher.verify(senha, hash_guardado)
