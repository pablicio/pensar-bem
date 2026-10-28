#include <stdio.h>

#define GRAUS(b) b / 16.0f

int main(void)
{
    int bruto = 117;
    printf("%.2f\n", GRAUS(bruto + 8));
    return 0;
}
