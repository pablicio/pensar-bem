public class SolicitacaoEncerradaException : InvalidOperationException
{
    public SolicitacaoEncerradaException(
        int id, StatusSolicitacao status)
        : base($"Solicitação {id} está {status}: sem mudanças.")
    {
        Id = id;
        Status = status;
    }

    public int Id { get; }
    public StatusSolicitacao Status { get; }
}
