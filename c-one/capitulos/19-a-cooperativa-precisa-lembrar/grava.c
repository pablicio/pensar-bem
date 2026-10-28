#include <stdio.h>

int main(void)
{
    FILE *f = fopen("leituras.txt", "w");
    if (f == NULL) {
        perror("leituras.txt");
        return 1;
    }

    fprintf(f, "T%03d %d %.1f\n", 47, 61, 3.8f);
    fprintf(f, "T%03d %d %.1f\n", 48, 54, 3.4f);

    fclose(f);
    return 0;
}
