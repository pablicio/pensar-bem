int desempacotar(const uint8_t b[PACOTE_TAM], Pacote *p)
{
    if (b[0] != PACOTE_INICIO) {
        return -1;
    }
    if (verificador(b, 11) != b[11]) {
        return -2;
    }
    Pacote q = {
        .tanque     = tira16(&b[1]),
        .seq        = b[3],
        .bruto      = (int16_t)tira16(&b[4]),
        .status     = b[6],
        .bateria_mv = tira16(&b[7]),
        .ligada_min = tira16(&b[9]),
    };
    if (q.tanque == 0) {
        return -3;
    }
    *p = q;
    return 0;
}
