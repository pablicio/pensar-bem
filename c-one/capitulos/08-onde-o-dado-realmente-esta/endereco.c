#include <stdio.h>

int main(void)
{
    int alarmes = 7;
    printf("valor:    %d\n", alarmes);
    printf("endereco: %p\n", (void *)&alarmes);
    printf("tamanho:  %zu\n", sizeof alarmes);
    return 0;
}
