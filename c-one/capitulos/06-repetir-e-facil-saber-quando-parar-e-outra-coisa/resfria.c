#include <stdio.h>

int main(void)
{
    float graus = 11.0f;
    int minutos = 0;

    while (graus > 4.0f) {
        graus = graus - 0.8f;
        minutos = minutos + 5;
    }
    printf("resfriou em %d minutos (%.1f graus)\n", minutos, graus);
    return 0;
}
