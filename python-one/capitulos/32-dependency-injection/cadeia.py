def get_session() -> Generator[Session, None, None]:
    ...


SessaoDep = Annotated[Session, Depends(get_session)]


def get_repo(session: SessaoDep) -> ProdutoRepositorioSQL:
    return ProdutoRepositorioSQL(session)


RepoDep = Annotated[ProdutoRepositorioSQL, Depends(get_repo)]


def get_servico(
    session: SessaoDep, repo: RepoDep
) -> ProdutoServico:
    return ProdutoServico(session, repo)


ServicoDep = Annotated[ProdutoServico, Depends(get_servico)]
