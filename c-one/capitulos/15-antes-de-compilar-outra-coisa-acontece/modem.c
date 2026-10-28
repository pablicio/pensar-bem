#include <stdio.h>
#include "modem.h"

int enviar_sms(const char *numero, const char *texto)
{
#ifdef SIMULADOR
    printf("[SIMULADO] para %s: %s\n", numero, texto);
    return 0;
#else
    return modem_at_enviar(numero, texto);
#endif
}
