#include <stdio.h>

int leituras_por_dia(int minutos_entre_leituras)
{
    return 24 * 60 / minutos_entre_leituras;
}

int main(void)
{
    printf("A cada 5 min: %d leituras\n", leituras_por_dia(5));
    printf("A cada 10 min: %d leituras\n", leituras_por_dia(10));
    return 0;
}
