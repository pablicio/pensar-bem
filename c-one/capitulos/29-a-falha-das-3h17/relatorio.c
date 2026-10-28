static void relatorio_atrasos(Tanque *tanques, int n, time_t inicio)
{
    for (int i = 0; i < n; i++) {
        const Tanque *t = &tanques[i];
        if (t->chegou > inicio && t->chegou - t->esperado > 90) {
            fprintf(arq_relatorio, "ATRASO T%03d %s (%lds)\n",
                    t->numero, t->fazenda,
                    (long)(t->chegou - t->esperado));
        }
    }
}
