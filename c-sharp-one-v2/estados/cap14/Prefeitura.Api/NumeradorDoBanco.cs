using Microsoft.EntityFrameworkCore;
using Prefeitura.Dominio;

namespace Prefeitura.Api;

public class NumeradorDoBanco(PrefeituraDbContext db) : INumerador
{
    public Protocolo Proximo()
    {
        var sequencial = db.Database
            .SqlQuery<int>($"""
                SELECT nextval('protocolo_sequencial') AS "Value"
                """)
            .Single();
        return new Protocolo(2027, sequencial);
    }
}
