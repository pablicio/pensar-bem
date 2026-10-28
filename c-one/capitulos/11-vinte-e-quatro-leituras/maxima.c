#include <stdio.h>

int main(void)
{
    float hora[24] = {
        3.4f, 3.5f, 3.4f, 3.6f, 3.5f, 6.1f, 5.2f, 4.4f,
        3.9f, 3.7f, 3.6f, 3.6f, 3.5f, 3.6f, 3.7f, 3.8f,
        3.6f, 6.4f, 5.5f, 4.6f, 3.9f, 3.7f, 3.6f, 3.5f
    };

    float maxima = hora[0];
    int quando = 0;
    for (int h = 1; h < 24; h++) {
        if (hora[h] > maxima) {
            maxima = hora[h];
            quando = h;
        }
    }
    printf("maxima: %.1f graus as %dh\n", maxima, quando);
    return 0;
}
