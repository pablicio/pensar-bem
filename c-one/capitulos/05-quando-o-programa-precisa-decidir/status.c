#include <stdio.h>

int main(void)
{
    char status = 'B';

    switch (status) {
    case 'N':
        printf("caixinha ok\n");
        break;
    case 'B':
        printf("bateria fraca: avisar tecnico\n");
        break;
    case 'R':
        printf("caixinha reiniciou\n");
        break;
    default:
        printf("status desconhecido: %c\n", status);
        break;
    }
    return 0;
}
