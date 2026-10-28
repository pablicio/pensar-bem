#include <stdio.h>
#include "pacote.h"

int main(void)
{
    Pacote p = { .tanque = 47, .seq = 12, .bruto = 61, .status = 0,
                 .bateria_mv = 3610, .ligada_min = 540 };
    uint8_t fio[PACOTE_TAM];
    empacotar(&p, fio);

    for (int i = 0; i < PACOTE_TAM; i++) {
        printf("%02x ", fio[i]);
    }
    printf("\n");

    Pacote volta;
    printf("ok: %d\n", desempacotar(fio, &volta));
    printf("tanque %u bruto %d\n", volta.tanque, volta.bruto);

    fio[5] ^= 0x02;   /* o rádio troca um bit */
    printf("estragado: %d\n", desempacotar(fio, &volta));
    return 0;
}
