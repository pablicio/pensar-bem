#include <stdio.h>
#include <stdbool.h>

struct tanque {
    int numero;
    char fazenda[48];
    float graus;
    char status;
    bool ativo;
};

int main(void)
{
    struct tanque t = {
        .numero = 47,
        .fazenda = "Boa Vista",
        .graus = 3.8f,
        .status = 'N',
        .ativo = true,
    };

    printf("T%03d %s %.1f %c\n",
           t.numero, t.fazenda, t.graus, t.status);
    t.graus = 7.9f;
    printf("agora: %.1f\n", t.graus);
    return 0;
}
