#include <stdio.h>

float media(const float v[], int n)
{
    float soma = 0.0f;
    for (int i = 0; i <= n; i++) {
        soma += v[i];
    }
    return soma / n;
}

int main(void)
{
    float horas[4] = {3.4f, 3.5f, 3.6f, 3.5f};
    float m = media(horas, 4);
    printf("media: %.2f\n", m);
    return 0;
}
