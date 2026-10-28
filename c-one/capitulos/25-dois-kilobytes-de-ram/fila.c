#include "fila.h"

void fila_poe(Fila *f, Leitura l)
{
    uint8_t fim = (uint8_t)((f->inicio + f->quantos) % FILA_CAP);
    f->itens[fim] = l;
    if (f->quantos < FILA_CAP) {
        f->quantos++;
    } else {
        f->inicio = (uint8_t)((f->inicio + 1) % FILA_CAP);
    }
}

bool fila_tira(Fila *f, Leitura *l)
{
    if (f->quantos == 0) {
        return false;
    }
    *l = f->itens[f->inicio];
    f->inicio = (uint8_t)((f->inicio + 1) % FILA_CAP);
    f->quantos--;
    return true;
}
