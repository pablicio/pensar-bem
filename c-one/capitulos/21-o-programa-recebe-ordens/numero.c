#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

int ler_inteiro(const char *texto, long minimo, long maximo,
                long *valor)
{
    char *fim;
    errno = 0;
    long n = strtol(texto, &fim, 10);
    if (fim == texto || *fim != '\0') {
        return -1;          /* não é número, ou tem lixo no fim */
    }
    if (errno == ERANGE || n < minimo || n > maximo) {
        return -1;          /* fora da faixa */
    }
    *valor = n;
    return 0;
}

int main(int argc, char *argv[])
{
    for (int i = 1; i < argc; i++) {
        long porta;
        if (ler_inteiro(argv[i], 1, 65535, &porta) == 0) {
            printf("%s -> %ld\n", argv[i], porta);
        } else {
            printf("%s -> invalido\n", argv[i]);
        }
    }
    return 0;
}
