#include <stdio.h>
#include <string.h>

int main(void)
{
    char cabecalho[24];
    int tanque = 163;

    strcpy(cabecalho, "Nossa Senhora Aparecida do Ribeirao Fundo");
    printf("[%s] tanque %d\n", cabecalho, tanque);
    return 0;
}
