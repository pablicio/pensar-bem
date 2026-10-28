#include <stdio.h>
#include <stdbool.h>

#define NORMAL   0
#define ATENCAO  1
#define CRITICO  2
#define IGNORAR  3

float converter(int bruto)
{
    return bruto / 16.0f;
}

bool em_resfriamento(int hora)
{
    return (hora >= 4 && hora < 7) || (hora >= 16 && hora < 19);
}

int classificar(int bruto, int hora)
{
    if (bruto == 1360) {
        return IGNORAR;
    }
    float graus = converter(bruto);
    if (graus > 7.0f) {
        return CRITICO;
    }
    if (graus > 4.0f && !em_resfriamento(hora)) {
        return ATENCAO;
    }
    return NORMAL;
}

int main(void)
{
    printf("%d\n", classificar(117, 10));
    printf("%d\n", classificar(96, 5));
    printf("%d\n", classificar(96, 10));
    printf("%d\n", classificar(1360, 4));
    return 0;
}
