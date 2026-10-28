#include <stdio.h>
#include "tanque.h"

int main(void)
{
    Tanque t = { .numero = 47, .fazenda = "Boa Vista",
                 .ativo = true };
    atualizar(&t, 117, 'R');
    printf("T%03d %.1f %c\n", t.numero, t.graus, t.status);
    printf("ativos: %d\n", contar_ativos(&t, 1));
    return 0;
}
