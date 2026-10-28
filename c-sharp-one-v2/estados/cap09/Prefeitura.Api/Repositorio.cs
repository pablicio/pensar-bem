using Prefeitura.Dominio;

namespace Prefeitura.Api;

public interface IRepositorioDeSolicitacoes
{
    Solicitacao? PorId(int id);
    IEnumerable<Solicitacao> Todas();
    void Adicionar(Solicitacao s);
}

public class RepositorioEmMemoria(List<Solicitacao> dados)
    : IRepositorioDeSolicitacoes
{
    public Solicitacao? PorId(int id) => dados.FirstOrDefault(s => s.Id == id);
    public IEnumerable<Solicitacao> Todas() => dados;
    public void Adicionar(Solicitacao s) => dados.Add(s);
}
