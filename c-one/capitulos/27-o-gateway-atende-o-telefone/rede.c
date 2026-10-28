#include <unistd.h>
#include <errno.h>
#include <stdint.h>

/* Lê exatamente n bytes. Devolve 1 se leu, 0 se a conexão
   terminou antes, -1 em erro (errno preenchido). */
int ler_exato(int fd, uint8_t *destino, size_t n)
{
    size_t lidos = 0;
    while (lidos < n) {
        ssize_t r = read(fd, destino + lidos, n - lidos);
        if (r > 0) {
            lidos += (size_t)r;
        } else if (r == 0) {
            return 0;
        } else if (errno != EINTR) {
            return -1;
        }
    }
    return 1;
}
