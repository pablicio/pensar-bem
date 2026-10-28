#include <stdio.h>

#define NUM_TANQUES 3

struct {
    float ultima_temp[NUM_TANQUES];
    int sms_enviados;
} g = { {3.4f, 3.6f, 3.5f}, 5 };

int main(void)
{
    for (int i = 0; i <= NUM_TANQUES; i++) {
        printf("tanque %d: %f\n", i, g.ultima_temp[i]);
    }
    return 0;
}
