#include <stdio.h>
#include <pthread.h>

void *atender(void *arg)
{
    int tanque = *(int *)arg;
    printf("atendendo tanque %d\n", tanque);
    return NULL;
}

int main(void)
{
    pthread_t t1, t2;
    int a = 47, b = 48;

    pthread_create(&t1, NULL, atender, &a);
    pthread_create(&t2, NULL, atender, &b);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("fim\n");
    return 0;
}
