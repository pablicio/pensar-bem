#include <stdio.h>

int main(void)
{
    int alarmes = 7;
    int *p = &alarmes;

    printf("alarmes: %d\n", alarmes);
    printf("p:       %p\n", (void *)p);
    printf("*p:      %d\n", *p);

    *p = 0;
    printf("alarmes: %d\n", alarmes);
    return 0;
}
