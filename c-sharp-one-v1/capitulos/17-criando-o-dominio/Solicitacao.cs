    public void Encaminhar(
        Secretaria destino, Servidor quem, string motivo)
    {
        if (Situacao is StatusSolicitacao.Resolvida
                     or StatusSolicitacao.Cancelada)
        {
            throw new InvalidOperationException(
                $"Solicitação {Id} está {Situacao}.");
        }

        var descricao = $"Encaminhada de {SecretariaAtual.Sigla} " +
                        $"para {destino.Sigla}: {motivo}";
        var registro = new Atendimento(DateTime.Now, quem, descricao);
        _atendimentos.Add(registro);
        SecretariaAtual = destino;
    }
