if (!porCpf.TryGetValue(cpf, out var cidadao))
{
    cidadao = new Cidadao(proximoId++, nome) { Cpf = cpf };
    porCpf[cpf] = cidadao;
}
