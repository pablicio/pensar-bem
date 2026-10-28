using Microsoft.EntityFrameworkCore;
using Prefeitura.Dominio;

namespace Prefeitura.Infraestrutura;

public class NumeradorDoBanco(PrefeituraDbContext db) : INumerador
{
    public async Task<Protocolo> ProximoAsync(
        CancellationToken cancelamento)
    {
        var sequencial = await db.Database
            .SqlQuery<int>($"""
                SELECT nextval('protocolo_sequencial') AS "Value"
                """)
            .SingleAsync(cancelamento);
        return new Protocolo(2027, sequencial);
    }
}
