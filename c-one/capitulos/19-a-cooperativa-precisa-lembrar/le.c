#include <stdio.h>

int main(void)
{
    FILE *f = fopen("leituras.txt", "r");
    if (f == NULL) {
        perror("leituras.txt");
        return 1;
    }

    char linha[64];
    while (fgets(linha, sizeof linha, f) != NULL) {
        int tanque, bruto;
        float graus;
        int lidos = sscanf(linha, "T%d %d %f",
                           &tanque, &bruto, &graus);
        if (lidos == 3) {
            printf("tanque %d: %.1f\n", tanque, graus);
        }
    }

    fclose(f);
    return 0;
}
