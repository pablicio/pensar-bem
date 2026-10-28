#include <stdio.h>
#include <string.h>
#include "../src/relatorio.h"

int main(void)
{
    Tanque t = { .numero = 163, .ativo = true,
                 .esperado = 1000, .chegou = 1200 };
    strcpy(t.fazenda, "Nossa Senhora Aparecida do Ribeirao Fundo");

    FILE *saida = tmpfile();
    relatorio_usar_arquivo(saida);
    relatorio_atrasos(&t, 1, 1100);
    printf("ok\n");
    return 0;
}
