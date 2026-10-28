#include <stdio.h>
#include "fila.h"

int main(void)
{
    static Fila f;
    for (uint16_t m = 0; m < 60 * 5; m += 5) {
        fila_poe(&f, (Leitura){ .instante = m, .bruto = 61 });
    }
    printf("guardadas: %d\n", f.quantos);

    Leitura l;
    fila_tira(&f, &l);
    printf("mais antiga: minuto %d\n", l.instante);
    return 0;
}
