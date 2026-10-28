#include <stdio.h>
#include <stdbool.h>

int main(void)
{
    int bruto = 96;
    int hora = 5;
    float graus = bruto / 16.0f;

    bool resfriando = (hora >= 4 && hora < 7) ||
                      (hora >= 16 && hora < 19);

    if (bruto == 1360) {
        printf("sensor reiniciou, leitura ignorada\n");
    } else if (graus > 7.0f) {
        printf("%.1f graus: CRITICO\n", graus);
    } else if (graus > 4.0f && !resfriando) {
        printf("%.1f graus: ATENCAO\n", graus);
    } else {
        printf("%.1f graus: normal\n", graus);
    }
    return 0;
}
