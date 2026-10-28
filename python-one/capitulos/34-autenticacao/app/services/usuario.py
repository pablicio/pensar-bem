def autenticar(self, email: str, senha: str) -> Usuario | None:
    usuario = self.repo.buscar_por_email(email.strip().lower())

    if usuario is None:
        gerar_hash(senha)      # gasta o mesmo tempo
        return None

    if not conferir_senha(senha, usuario.senha_hash):
        return None

    if not usuario.ativo:
        return None

    return usuario
