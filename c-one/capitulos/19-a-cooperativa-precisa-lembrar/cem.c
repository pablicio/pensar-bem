#include <stdio.h>

int main(void)
{
    int n = 100;
    FILE *t = fopen("cem.txt", "w");
    FILE *b = fopen("cem.bin", "wb");
    if (t == NULL || b == NULL) {
        return 1;
    }
    fprintf(t, "%d", n);
    fwrite(&n, sizeof n, 1, b);
    fclose(t);
    fclose(b);
    return 0;
}
