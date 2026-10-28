#include <stdio.h>

int main(void)
{
    int bruto = 0;
    printf("valor bruto: ");
    if (scanf("%d", &bruto) == 1) {
        printf("%.2f graus\n", bruto / 16.0f);
    } else {
        printf("isso nao e um numero\n");
    }
    return 0;
}
