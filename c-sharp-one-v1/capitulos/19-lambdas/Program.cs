var sigla = "SEOB";
Func<Solicitacao, bool> daSecretaria =
    p => p.SecretariaAtual.Sigla == sigla;

sigla = "SEMA";
var resultado = Filtros.Filtrar(pedidos, daSecretaria);
