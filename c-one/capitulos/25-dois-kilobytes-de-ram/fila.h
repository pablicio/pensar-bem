#ifndef FILA_H
#define FILA_H

#include <stdint.h>
#include <stdbool.h>

#define FILA_CAP 48

typedef struct {
    uint16_t instante;  /* minutos desde que a caixinha ligou */
    int16_t bruto;
} Leitura;

typedef struct {
    Leitura itens[FILA_CAP];
    uint8_t inicio;     /* próxima a sair */
    uint8_t quantos;
} Fila;

void fila_poe(Fila *f, Leitura l);
bool fila_tira(Fila *f, Leitura *l);

#endif
