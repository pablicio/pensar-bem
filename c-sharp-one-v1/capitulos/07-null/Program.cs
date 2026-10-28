int? protocolo = null;          // registrada, ainda sem protocolo
Console.WriteLine(protocolo.HasValue);

protocolo = 4213;               // documentos conferidos
Console.WriteLine(protocolo.HasValue);
Console.WriteLine(protocolo.Value);
