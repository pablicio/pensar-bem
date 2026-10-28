var anota = new NotificadorQueAnota();
var balcao = new Balcao(new Numerador(null), anota);

balcao.Protocolar(pedidoDaMaria);

var (nome, mensagem) = anota.Enviados.Single();
var destinoOk = nome == "MARIA G SOUZA";
var numeroOk = mensagem.Contains("NE-2027-000001");
Console.WriteLine(destinoOk ? "ok" : "ERRO: destinatário");
Console.WriteLine(numeroOk ? "ok" : "ERRO: número");
