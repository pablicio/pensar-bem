var numerador = new Numerador(ultimoEmitido: null);

INotificador notificador = new NotificadorConsole();
var balcao = new Balcao(numerador, notificador);

balcao.Protocolar(pedidoDaMaria);
