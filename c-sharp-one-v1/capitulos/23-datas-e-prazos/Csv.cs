using System.Globalization;

var ptBr = CultureInfo.GetCultureInfo("pt-BR");
var data = DateOnly.ParseExact("27/11/26", "dd/MM/yy", ptBr);
Console.WriteLine(data.Year);
