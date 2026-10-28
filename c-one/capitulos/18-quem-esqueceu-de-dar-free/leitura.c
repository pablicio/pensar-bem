int interpretar_linha(const char *linha, int *tanque, int *bruto)
{
    int resultado = 0;
    char *copia = malloc(strlen(linha) + 1);
    if (copia == NULL) {
        return -1;
    }
    strcpy(copia, linha);

    if (copia[0] != 'T') {
        resultado = -2;
        goto fim;
    }
    if (sscanf(copia + 1, "%d %d", tanque, bruto) != 2) {
        resultado = -3;
        goto fim;
    }

fim:
    free(copia);
    return resultado;
}
