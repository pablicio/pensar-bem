#include <stdio.h>
#include <stdint.h>

int main(void)
{
    uint16_t n = 0x0550;
    uint8_t *b = (uint8_t *)&n;
    printf("primeiro byte: 0x%02x\n", b[0]);
    printf("segundo byte:  0x%02x\n", b[1]);
    return 0;
}
