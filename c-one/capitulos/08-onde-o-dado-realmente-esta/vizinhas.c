#include <stdio.h>

int main(void)
{
    int bruto = 61;
    int hora = 5;
    char status = 'N';
    printf("bruto:  %p\n", (void *)&bruto);
    printf("hora:   %p\n", (void *)&hora);
    printf("status: %p\n", (void *)&status);
    return 0;
}
