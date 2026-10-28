#include <stdio.h>

int main(void)
{
    int bruto = 117;
    float graus = bruto / 16.0f;

    if (bruto == 1360) {
        printf("sensor reiniciou, leitura ignorada\n");
    } else if (graus > 7.0f) {
        printf("%.1f graus: CRITICO\n", graus);
    } else if (graus > 4.0f) {
        printf("%.1f graus: ATENCAO\n", graus);
    } else {
        printf("%.1f graus: normal\n", graus);
    }
    return 0;
}
