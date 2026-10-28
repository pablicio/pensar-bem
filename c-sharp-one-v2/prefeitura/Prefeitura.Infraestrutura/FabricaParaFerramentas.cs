using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace Prefeitura.Infraestrutura;

// Usada só pelo dotnet ef (migrations, bundle), sem subir a API.
public class FabricaParaFerramentas
    : IDesignTimeDbContextFactory<PrefeituraDbContext>
{
    public PrefeituraDbContext CreateDbContext(string[] args)
    {
        var conexao = Environment.GetEnvironmentVariable(
                          "ConnectionStrings__Principal")
                      ?? "Host=localhost;Database=prefeitura";
        var opcoes =
            new DbContextOptionsBuilder<PrefeituraDbContext>()
                .UseNpgsql(conexao)
                .UseSnakeCaseNamingConvention()
                .Options;
        return new PrefeituraDbContext(opcoes);
    }
}
