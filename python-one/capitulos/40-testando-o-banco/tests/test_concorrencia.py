from threading import Barrier, Thread


def test_duas_vendas_simultaneas(engine):
    largada = Barrier(2)

    def vender():
        with Session(engine) as sessao:
            largada.wait()
            with sessao.begin():
                produto = sessao.scalars(
                    select(Produto)
                    .where(Produto.id == 1)
                    .with_for_update()
                ).one()
                if produto.estoque >= 10:
                    produto.estoque -= 10

    threads = [Thread(target=vender) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    with Session(engine) as sessao:
        produto = sessao.get(Produto, 1)
        assert produto.estoque == 80
