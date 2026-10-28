var feriados = new HashSet<DateOnly>
{
    new(2027, 1, 1),
    new(2027, 1, 20),   // São Sebastião, padroeiro
    new(2027, 4, 21),
    new(2027, 5, 1),
    new(2027, 6, 1),    // aniversário da cidade
};

var pedido = new DateOnly(2027, 5, 28);
var prazo = Prazos.SomarDiasUteis(pedido, 2, feriados);
Console.WriteLine($"{prazo} ({prazo.DayOfWeek})");
