var abertos = pedidos
    .Where(p => p.Situacao == StatusSolicitacao.Aberta);

pedidos.Add(new Solicitacao(9999, maria, "BURACO", obras));

Console.WriteLine(abertos.Count());
