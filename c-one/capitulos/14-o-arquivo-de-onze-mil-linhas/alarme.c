#include <stdio.h>
#include "alarme.h"

static int sms_enviados = 0;

static bool modem_pronto(void)
{
    return true;   /* simulação */
}

void disparar_sms(int tanque, float graus)
{
    if (modem_pronto()) {
        printf("SMS T%03d %.1f\n", tanque, graus);
        sms_enviados++;
    }
}

int total_sms(void)
{
    return sms_enviados;
}
