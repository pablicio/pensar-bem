#include <stdio.h>

int main(void)
{
    char sms[40];
    const char *fazenda = "Nossa Senhora Aparecida do Ribeirao Fundo";
    float graus = 7.9f;

    int precisava = snprintf(sms, sizeof sms, "%s %.1fC",
                             fazenda, graus);
    printf("[%s]\n", sms);
    if (precisava >= (int)sizeof sms) {
        printf("cortado: precisava de %d\n", precisava);
    }
    return 0;
}
