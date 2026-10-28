#include <stdio.h>

int ler_sensor(void)
{
    int bruto = 1360;
    return bruto;
}

int nivel_do_status(char status)
{
    int nivel;
    if (status == 'N') {
        nivel = 0;
    } else if (status == 'B') {
        nivel = 1;
    }
    return nivel;
}

int main(void)
{
    ler_sensor();
    printf("nivel: %d\n", nivel_do_status('R'));
    return 0;
}
