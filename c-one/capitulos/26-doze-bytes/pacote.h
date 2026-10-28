#ifndef PACOTE_H
#define PACOTE_H

#include <stdint.h>

#define PACOTE_TAM    12
#define PACOTE_INICIO 0xA5

typedef struct {
    uint16_t tanque;
    uint8_t seq;
    int16_t bruto;
    uint8_t status;
    uint16_t bateria_mv;
    uint16_t ligada_min;
} Pacote;

void empacotar(const Pacote *p, uint8_t b[PACOTE_TAM]);
int desempacotar(const uint8_t b[PACOTE_TAM], Pacote *p);

#endif
