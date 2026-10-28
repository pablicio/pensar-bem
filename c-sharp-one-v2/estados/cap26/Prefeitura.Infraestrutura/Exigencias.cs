using Microsoft.Extensions.Configuration;

namespace Prefeitura.Infraestrutura;

public static class Exigencias
{
    public static string Exigir(
        this IConfiguration configuracao, string chave, int minimo = 1)
    {
        var valor = configuracao[chave];
        if (valor is null || valor.Length < minimo)
        {
            throw new InvalidOperationException(
                $"Configuração ausente ou curta demais: {chave}. " +
                $"Defina a variável de ambiente " +
                $"{chave.Replace(":", "__")}.");
        }
        return valor;
    }
}
