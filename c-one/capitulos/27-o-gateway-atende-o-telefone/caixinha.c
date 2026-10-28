#include <stdio.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "pacote.h"

int main(void)
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in end = {0};
    end.sin_family = AF_INET;
    end.sin_port = htons(7070);
    inet_pton(AF_INET, "127.0.0.1", &end.sin_addr);

    if (connect(fd, (struct sockaddr *)&end, sizeof end) < 0) {
        perror("connect");
        return 1;
    }

    for (int i = 0; i < 3; i++) {
        Pacote p = { .tanque = 47, .seq = (uint8_t)i,
                     .bruto = (int16_t)(61 + i), .bateria_mv = 3610,
                     .ligada_min = (uint16_t)(i * 5) };
        uint8_t fio[PACOTE_TAM];
        empacotar(&p, fio);
        if (write(fd, fio, sizeof fio) != (ssize_t)sizeof fio) {
            perror("write");
            return 1;
        }
        sleep(1);
    }
    close(fd);
    return 0;
}
