#include <stdio.h>
#include <errno.h>
#include <string.h>
#include "historico.h"

int gravar_registro(FILE *f, const Registro *r)
{
    if (fwrite(r, sizeof *r, 1, f) != 1) {
        return -1;
    }
    if (fflush(f) != 0) {
        return -1;
    }
    return 0;
}
