#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int numero;
    char fazenda[48];
    float graus;
    char status;
    bool ativo;
} Tanque;

void atualizar(Tanque *t, int bruto, char status)
{
    t->graus = bruto / 16.0f;
    t->status = status;
}

void mostrar(const Tanque *t)
{
    printf("T%03d %s %.1f %c\n",
           t->numero, t->fazenda, t->graus, t->status);
}

int main(void)
{
    Tanque t = { .numero = 47, .fazenda = "Boa Vista" };
    atualizar(&t, 117, 'R');
    mostrar(&t);
    return 0;
}
