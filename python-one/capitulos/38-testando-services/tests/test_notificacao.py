from unittest.mock import Mock


def test_avisa_o_produtor_quando_o_estoque_zera():
    notificador = Mock()
    servico = ProdutoServico(
        SessaoFalsa(),
        RepositorioFalso(),
        notificador=notificador,
    )
    produto = servico.criar("Tomate", Decimal("8.90"), 10)

    servico.vender(produto.id, 10)

    notificador.enviar.assert_called_once()
    (destinatario, mensagem), _ = notificador.enviar.call_args
    assert "Tomate" in mensagem
