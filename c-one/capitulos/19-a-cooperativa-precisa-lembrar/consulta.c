#include <stdio.h>
#include "historico.h"

#define TANQUES_POR_INSTANTE 212

int consultar(FILE *f, long indice_instante, int tanque, Registro *r)
{
    long n = indice_instante * TANQUES_POR_INSTANTE + (tanque - 1);
    long posicao = n * (long)sizeof *r;
    if (fseek(f, posicao, SEEK_SET) != 0) {
        return -1;
    }
    if (fread(r, sizeof *r, 1, f) != 1) {
        return -1;
    }
    return 0;
}
