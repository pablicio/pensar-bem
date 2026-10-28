#include <stdio.h>
#include <stdint.h>
#include "status.h"

int main(void)
{
    uint8_t status = 0;

    status |= ST_REINICIOU;               /* liga */
    status |= ST_BATERIA;                 /* liga */
    printf("0x%02x\n", status);

    if (status & ST_BATERIA) {            /* testa */
        printf("bateria fraca\n");
    }

    status &= (uint8_t)~ST_REINICIOU;     /* desliga */
    printf("0x%02x\n", status);

    status ^= ST_TAMPA;                   /* inverte */
    printf("0x%02x\n", status);
    return 0;
}
