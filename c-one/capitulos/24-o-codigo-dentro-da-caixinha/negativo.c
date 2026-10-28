#include <stdio.h>
#include <stdint.h>

int main(void)
{
    uint8_t lsb = 0xC0, msb = 0xFF;
    uint16_t sem_sinal = (uint16_t)((msb << 8) | lsb);
    int16_t com_sinal = (int16_t)sem_sinal;
    printf("%u %d %.2f\n", sem_sinal, com_sinal, com_sinal / 16.0f);
    return 0;
}
