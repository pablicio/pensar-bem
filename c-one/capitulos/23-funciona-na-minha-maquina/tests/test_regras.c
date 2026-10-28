#include <stdio.h>
#include "../src/regras.h"

static int falhas = 0;

#define CONFERE(cond) \
    do { \
        if (!(cond)) { \
            printf("FALHOU %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            falhas++; \
        } \
    } while (0)

int main(void)
{
    CONFERE(classificar(56, 10) == NORMAL);      /* 3,5 graus */
    CONFERE(classificar(64, 10) == NORMAL);      /* 4,0: no limite */
    CONFERE(classificar(65, 10) == ATENCAO);     /* 4,06 */
    CONFERE(classificar(96, 5) == NORMAL);       /* 6,0 na ordenha */
    CONFERE(classificar(96, 7) == ATENCAO);      /* 6,0 às 7h */
    CONFERE(classificar(113, 5) == CRITICO);     /* 7,06 na ordenha */
    CONFERE(classificar(1360, 4) == IGNORAR);    /* sensor ligando */

    if (falhas == 0) {
        printf("ok\n");
    }
    return falhas == 0 ? 0 : 1;
}
