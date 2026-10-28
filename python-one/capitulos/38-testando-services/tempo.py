def test_promocao_expira(monkeypatch):
    congelado = datetime(2026, 3, 14, tzinfo=timezone.utc)
    monkeypatch.setattr(
        "app.services.produto.agora", lambda: congelado
    )
    ...
