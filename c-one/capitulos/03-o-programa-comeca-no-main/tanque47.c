/* tanque47.c - mostra quantas leituras o tanque 47 manda por dia.
   Uma leitura a cada 5 minutos. */
#include <stdio.h>

int main(void)
{
    // 12 leituras por hora, 24 horas
    printf("Tanque %d: %d leituras hoje\n", 47, 12 * 24);
    return 0;
}
