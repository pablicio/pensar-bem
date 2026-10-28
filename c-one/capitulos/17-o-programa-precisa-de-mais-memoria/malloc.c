#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int n = 255;
    float *graus = malloc(n * sizeof *graus);
    if (graus == NULL) {
        fprintf(stderr, "sem memoria\n");
        return 1;
    }

    for (int i = 0; i < n; i++) {
        graus[i] = 3.5f;
    }
    printf("ultimo: %.1f\n", graus[n - 1]);

    free(graus);
    return 0;
}
