#include <stdio.h>
#include <errno.h>
#include <string.h>

int main(void)
{
    FILE *f = fopen("/nao/existe/historico.bin", "rb");
    if (f == NULL) {
        int erro = errno;
        printf("errno = %d\n", erro);
        printf("strerror: %s\n", strerror(erro));
        perror("historico");
        return 1;
    }
    fclose(f);
    return 0;
}
