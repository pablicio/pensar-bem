#include <stdio.h>

void zerar(int contador)
{
    printf("contador em %p vale %d\n", (void *)&contador, contador);
    contador = 0;
    printf("contador em %p vale %d\n", (void *)&contador, contador);
}

int main(void)
{
    int alarmes = 7;
    printf("alarmes  em %p vale %d\n", (void *)&alarmes, alarmes);
    zerar(alarmes);
    printf("alarmes  em %p vale %d\n", (void *)&alarmes, alarmes);
    return 0;
}
