public static StatusSolicitacao? StatusDoSip(string texto) =>
    texto switch
    {
        "ABERTO" or "ABERTA" => Aberta,
        "EM ANALISE" or "EM ANÁLISE" => EmAnalise,
        "ATENDIMENTO" => EmAtendimento,
        "ENCERRADO" => Resolvida,
        "CANCELADO" => Cancelada,
        _ => null
    };
