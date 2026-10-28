#include <pthread.h>

static pthread_mutex_t trava = PTHREAD_MUTEX_INITIALIZER;
static long leituras_hoje = 0;

void registrar_leitura(const Pacote *p)
{
    pthread_mutex_lock(&trava);
    Tanque *t = procurar(tanques, n_tanques, p->tanque);
    if (t != NULL) {
        t->graus = p->bruto / 16.0f;
        t->status = p->status;
    }
    leituras_hoje++;
    pthread_mutex_unlock(&trava);
}

long total_leituras(void)
{
    pthread_mutex_lock(&trava);
    long n = leituras_hoje;
    pthread_mutex_unlock(&trava);
    return n;
}
