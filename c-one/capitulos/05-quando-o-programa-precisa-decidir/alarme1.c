#include <stdio.h>

int main(void)
{
    int bruto = 117;
    float graus = bruto / 16.0f;

    if (graus > 4.0f) {
        printf("%.1f graus: ALARME\n", graus);
    }
    printf("leitura processada\n");
    return 0;
}
