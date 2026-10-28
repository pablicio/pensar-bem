    public void Protocolar(int numero)
    {
        if (Protocolo is not null)
        {
            throw new InvalidOperationException(
                $"Solicitação {Id} já tem o protocolo {Protocolo}.");
        }
        Protocolo = numero;
    }

    public void IniciarAtendimento()
    {
        if (Situacao != "ABERTA" || Protocolo is null)
        {
            var numero = Protocolo?.ToString() ?? "nenhum";
            throw new InvalidOperationException(
                $"Solicitação {Id} não pode entrar em atendimento: " +
                $"situação {Situacao}, protocolo {numero}.");
        }
        Situacao = "EM ATENDIMENTO";
    }

    public void Cancelar()
    {
        if (Situacao is "RESOLVIDA" or "CANCELADA")
        {
            throw new InvalidOperationException(
                $"Solicitação {Id} já está {Situacao}.");
        }
        Situacao = "CANCELADA";
    }
