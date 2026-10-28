#include "tanque.h"

float converter(int bruto)
{
    return bruto / 16.0f;
}

void atualizar(Tanque *t, int bruto, char status)
{
    t->graus = converter(bruto);
    t->status = status;
}

int contar_ativos(const Tanque t[], int n)
{
    int conta = 0;
    for (int i = 0; i < n; i++) {
        if (t[i].ativo) {
            conta++;
        }
    }
    return conta;
}
