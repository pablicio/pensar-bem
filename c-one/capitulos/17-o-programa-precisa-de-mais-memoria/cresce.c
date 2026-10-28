#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int capacidade = 4;
    int usados = 0;
    int *numeros = malloc(capacidade * sizeof *numeros);
    if (numeros == NULL) {
        return 1;
    }

    for (int t = 1; t <= 10; t++) {
        if (usados == capacidade) {
            int nova = capacidade * 2;
            int *maior = realloc(numeros, nova * sizeof *numeros);
            if (maior == NULL) {
                free(numeros);
                return 1;
            }
            numeros = maior;
            capacidade = nova;
            printf("cresceu para %d\n", capacidade);
        }
        numeros[usados++] = t;
    }

    printf("%d tanques, capacidade %d\n", usados, capacidade);
    free(numeros);
    return 0;
}
