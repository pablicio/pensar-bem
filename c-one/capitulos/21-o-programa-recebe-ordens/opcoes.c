#include <stdio.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    const char *cadastro;
    const char *simular;
    long porta;
    bool verboso;
} Opcoes;

static void uso(const char *nome)
{
    fprintf(stderr,
            "uso: %s --cadastro ARQ [--porta N] [--simular LOG]"
            " [-v]\n",
            nome);
}

int ler_opcoes(int argc, char *argv[], Opcoes *op)
{
    *op = (Opcoes){ .porta = 7070 };
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-v") == 0) {
            op->verboso = true;
        } else if (i + 1 >= argc) {
            return -1;      /* toda opção abaixo pede um valor */
        } else if (strcmp(argv[i], "--cadastro") == 0) {
            op->cadastro = argv[++i];
        } else if (strcmp(argv[i], "--simular") == 0) {
            op->simular = argv[++i];
        } else if (strcmp(argv[i], "--porta") == 0) {
            if (ler_inteiro(argv[++i], 1, 65535, &op->porta) != 0) {
                return -1;
            }
        } else {
            return -1;
        }
    }
    return op->cadastro != NULL ? 0 : -1;
}
