public static class Filtros
{
    public static List<Solicitacao> Filtrar(
        List<Solicitacao> pedidos, Func<Solicitacao, bool> criterio)
    {
        var resultado = new List<Solicitacao>();
        foreach (var p in pedidos)
        {
            if (criterio(p))
            {
                resultado.Add(p);
            }
        }
        return resultado;
    }
}
