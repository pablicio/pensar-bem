public class NotificadorMultiplo : INotificador
{
    private readonly List<INotificador> _todos;

    public NotificadorMultiplo(params INotificador[] todos) =>
        _todos = [.. todos];

    public void Enviar(Cidadao destinatario, string mensagem)
    {
        foreach (var n in _todos)
        {
            n.Enviar(destinatario, mensagem);
        }
    }
}
