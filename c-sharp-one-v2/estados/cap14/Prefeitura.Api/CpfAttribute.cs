using System.ComponentModel.DataAnnotations;

namespace Prefeitura.Api;

public class CpfAttribute : ValidationAttribute
{
    public CpfAttribute() =>
        ErrorMessage = "CPF inválido: 11 dígitos, sem pontos.";

    public override bool IsValid(object? value)
    {
        if (value is null)
        {
            return true;            // obrigatório é outro atributo
        }
        if (value is not string cpf || cpf.Length != 11
            || !cpf.All(char.IsAsciiDigit)
            || cpf.Distinct().Count() == 1)
        {
            return false;
        }
        return cpf[9] - '0' == Digito(cpf, 9)
            && cpf[10] - '0' == Digito(cpf, 10);
    }

    private static int Digito(string cpf, int quantos)
    {
        var soma = 0;
        for (var i = 0; i < quantos; i++)
        {
            soma += (cpf[i] - '0') * (quantos + 1 - i);
        }
        var resto = soma % 11;
        return resto < 2 ? 0 : 11 - resto;
    }
}
