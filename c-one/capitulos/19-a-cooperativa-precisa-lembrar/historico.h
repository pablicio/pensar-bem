#ifndef HISTORICO_H
#define HISTORICO_H

#include <stdint.h>

typedef struct {
    int32_t instante;   /* minutos desde 01/01/2026 */
    int16_t tanque;
    int16_t bruto;
} Registro;

#endif
