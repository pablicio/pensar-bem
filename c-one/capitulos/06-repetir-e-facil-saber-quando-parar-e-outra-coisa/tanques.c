#include <stdio.h>

int main(void)
{
    int verificados = 0;

    for (int t = 1; t <= 212; t++) {
        verificados++;
    }
    printf("tanques verificados: %d\n", verificados);
    return 0;
}
