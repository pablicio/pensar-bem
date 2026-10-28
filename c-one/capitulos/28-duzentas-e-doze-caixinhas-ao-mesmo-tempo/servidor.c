static void *atender(void *arg)
{
    int con = *(int *)arg;
    free(arg);

    uint8_t fio[PACOTE_TAM];
    Pacote p;
    while (ler_exato(con, fio, sizeof fio) == 1) {
        if (desempacotar(fio, &p) == 0) {
            registrar_leitura(&p);
        }
    }
    close(con);
    return NULL;
}

    for (;;) {
        int con = accept(escuta, NULL, NULL);
        if (con < 0) {
            continue;
        }
        int *arg = malloc(sizeof *arg);
        if (arg == NULL) {
            close(con);
            continue;
        }
        *arg = con;
        pthread_t t;
        if (pthread_create(&t, NULL, atender, arg) != 0) {
            free(arg);
            close(con);
            continue;
        }
        pthread_detach(t);
    }
