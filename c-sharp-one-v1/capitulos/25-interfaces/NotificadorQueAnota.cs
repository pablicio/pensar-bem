public class NotificadorQueAnota : INotificador
{
    public List<(string Nome, string Mensagem)> Enviados { get; }
        = [];

    public void Enviar(Cidadao destinatario, string mensagem) =>
        Enviados.Add((destinatario.Nome, mensagem));
}
