#define NIVEL_DESCONHECIDO (-1)

int nivel_do_status(char status)
{
    int nivel = NIVEL_DESCONHECIDO;
    switch (status) {
    case 'N':
        nivel = 0;
        break;
    case 'B':
        nivel = 1;
        break;
    case 'R':
        nivel = 0;   /* reiniciou: a temperatura decide */
        break;
    default:
        break;
    }
    return nivel;
}
