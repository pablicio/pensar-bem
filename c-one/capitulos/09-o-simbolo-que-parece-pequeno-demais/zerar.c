#include <stdio.h>

void zerar(int *contador)
{
    *contador = 0;
}

int main(void)
{
    int alarmes = 7;
    zerar(&alarmes);
    printf("alarmes: %d\n", alarmes);
    return 0;
}
