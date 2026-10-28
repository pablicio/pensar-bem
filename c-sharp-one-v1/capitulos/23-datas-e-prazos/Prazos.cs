public static class Prazos
{
    public static DateOnly SomarDiasUteis(
        DateOnly inicio, int dias, IReadOnlySet<DateOnly> feriados)
    {
        var data = inicio;
        var contados = 0;

        while (contados < dias)
        {
            data = data.AddDays(1);

            var fimDeSemana = data.DayOfWeek
                is DayOfWeek.Saturday or DayOfWeek.Sunday;
            if (fimDeSemana)
            {
                continue;
            }
            if (feriados.Contains(data))
            {
                continue;
            }
            contados++;
        }
        return data;
    }
}
