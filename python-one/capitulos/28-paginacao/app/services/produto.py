def listar(self, pagina: int = 1, tamanho: int = 20) -> Pagina:
    tamanho = max(1, min(tamanho, 100))
    pagina = max(1, pagina)

    itens = self.repo.listar(
        limite=tamanho, deslocamento=(pagina - 1) * tamanho
    )
    total = self.repo.contar()

    return Pagina(
        itens=itens, total=total, pagina=pagina, tamanho=tamanho
    )
