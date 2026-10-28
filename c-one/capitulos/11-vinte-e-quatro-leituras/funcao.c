#include <stdio.h>

float maxima(const float valores[], int n)
{
    float m = valores[0];
    for (int i = 1; i < n; i++) {
        if (valores[i] > m) {
            m = valores[i];
        }
    }
    return m;
}

int main(void)
{
    float hora[24] = {3.4f, 3.5f, 6.1f, 4.4f};
    printf("maxima: %.1f\n", maxima(hora, 24));
    return 0;
}
