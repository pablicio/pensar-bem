#include <stdio.h>
#include <stdbool.h>

bool enviar_sms(int tentativa)
{
    /* simulação: o modem só consegue na terceira */
    return tentativa == 3;
}

int main(void)
{
    int tentativa = 0;
    bool enviado;

    do {
        tentativa++;
        enviado = enviar_sms(tentativa);
        printf("tentativa %d: %d\n", tentativa, enviado);
    } while (!enviado && tentativa < 3);

    if (!enviado) {
        printf("SMS NAO ENVIADO\n");
    }
    return 0;
}
