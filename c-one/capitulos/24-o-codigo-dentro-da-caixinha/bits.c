#include <stdio.h>
#include <stdint.h>

void mostrar_bits(uint8_t b)
{
    for (int i = 7; i >= 0; i--) {
        putchar((b >> i) & 1 ? '1' : '0');
    }
    putchar('\n');
}

int main(void)
{
    mostrar_bits(5);
    mostrar_bits(0x80);
    mostrar_bits(255);
    return 0;
}
