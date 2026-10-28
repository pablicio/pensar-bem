public class Balcao
{
    private readonly Numerador _numerador;
    private readonly INotificador _notificador;

    public Balcao(Numerador numerador, INotificador notificador)
    {
        _numerador = numerador;
        _notificador = notificador;
    }

    public void Protocolar(Solicitacao s)
    {
        var protocolo = _numerador.Proximo();
        s.Protocolar(protocolo);
        var mensagem = $"Seu protocolo: {protocolo}";
        _notificador.Enviar(s.Solicitante, mensagem);
    }
}
