var obras = new Secretaria("SEOB", "Obras");
var meioAmb = new Secretaria("SEMA", "Meio Ambiente");
var paulo = new Servidor("10442", "PAULO R MENDES", obras);
var maria = new Cidadao(1, "MARIA G SOUZA");

var pedido = new Solicitacao(4211, maria, "ÁRVORE NA FIAÇÃO", obras);
pedido.Encaminhar(meioAmb, paulo, "poda é do Meio Ambiente");

Console.WriteLine(pedido.SecretariaAtual.Nome);
foreach (var a in pedido.Atendimentos)
{
    Console.WriteLine($"{a.Quem.Nome}: {a.Descricao}");
}
