#include <stdlib.h>
#include "tanque.h"

Tanque *criar_tanques(int n)
{
    Tanque *lista = calloc(n, sizeof *lista);
    if (lista == NULL) {
        return NULL;
    }
    for (int i = 0; i < n; i++) {
        lista[i].numero = i + 1;
    }
    return lista;
}
