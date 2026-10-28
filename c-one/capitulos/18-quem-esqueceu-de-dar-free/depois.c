#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *contador = malloc(sizeof *contador);
    if (contador == NULL) {
        return 1;
    }
    *contador = 7;
    free(contador);
    printf("%d\n", *contador);
    return 0;
}
