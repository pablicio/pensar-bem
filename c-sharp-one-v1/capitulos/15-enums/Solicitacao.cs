private static bool Permitida(
    StatusSolicitacao de, StatusSolicitacao para) =>
    (de, para) switch
    {
        (Aberta, EmAnalise) => true,
        (EmAnalise, EmAtendimento) => true,
        (EmAtendimento, Resolvida) => true,
        (Resolvida, _) => false,
        (Cancelada, _) => false,
        (_, Cancelada) => true,
        _ => false
    };
