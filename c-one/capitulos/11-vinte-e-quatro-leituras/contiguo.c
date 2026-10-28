#include <stdio.h>

int main(void)
{
    float hora[4] = {3.4f, 3.5f, 3.4f, 3.6f};
    for (int h = 0; h < 4; h++) {
        printf("hora[%d] em %p\n", h, (void *)&hora[h]);
    }
    printf("sizeof hora: %zu\n", sizeof hora);
    return 0;
}
