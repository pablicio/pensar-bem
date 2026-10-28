#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int numero;
    char fazenda[48];
    float graus;
    char status;
    bool ativo;
} Tanque;

int main(void)
{
    Tanque tanques[] = {
        { .numero = 46, .fazenda = "Santa Rita",
          .graus = 6.1f, .ativo = true },
        { .numero = 47, .fazenda = "Boa Vista",
          .graus = 3.5f, .ativo = true },
        { .numero = 101, .fazenda = "Lourenco",
          .graus = 0.0f, .ativo = false },
    };
    int n = sizeof tanques / sizeof tanques[0];

    for (int i = 0; i < n; i++) {
        if (!tanques[i].ativo) {
            continue;
        }
        printf("T%03d %-12s %.1f\n", tanques[i].numero,
               tanques[i].fazenda, tanques[i].graus);
    }
    return 0;
}
