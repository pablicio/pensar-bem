#include <stdio.h>

int main(void)
{
    float hora[24] = {0};

    hora[0] = 3.4f;
    hora[1] = 3.5f;
    hora[5] = 6.1f;

    printf("0h: %.1f\n", hora[0]);
    printf("5h: %.1f\n", hora[5]);
    printf("9h: %.1f\n", hora[9]);
    return 0;
}
