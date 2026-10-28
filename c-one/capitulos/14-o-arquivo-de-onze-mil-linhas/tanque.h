#ifndef TANQUE_H
#define TANQUE_H

#include <stdbool.h>

#define NUM_TANQUES 212

typedef struct {
    int numero;
    char fazenda[48];
    float graus;
    char status;
    bool ativo;
} Tanque;

float converter(int bruto);
void atualizar(Tanque *t, int bruto, char status);
int contar_ativos(const Tanque t[], int n);

#endif
