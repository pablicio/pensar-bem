#include <stdio.h>
#include <stdbool.h>

bool interpretar(int bruto, char letra, float *graus, char *status)
{
    if (bruto == 1360) {
        return false;
    }
    *graus = bruto / 16.0f;
    *status = letra;
    return true;
}

int main(void)
{
    float graus = 0.0f;
    char status = '?';

    if (interpretar(117, 'R', &graus, &status)) {
        printf("%.1f graus, status %c\n", graus, status);
    } else {
        printf("leitura descartada\n");
    }

    if (interpretar(1360, 'R', &graus, &status)) {
        printf("%.1f graus, status %c\n", graus, status);
    } else {
        printf("leitura descartada\n");
    }
    return 0;
}
