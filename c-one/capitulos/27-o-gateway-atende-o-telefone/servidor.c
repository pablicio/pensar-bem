#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main(void)
{
    int escuta = socket(AF_INET, SOCK_STREAM, 0);
    if (escuta < 0) {
        perror("socket");
        return 1;
    }

    int sim = 1;
    setsockopt(escuta, SOL_SOCKET, SO_REUSEADDR, &sim, sizeof sim);

    struct sockaddr_in end = {0};
    end.sin_family = AF_INET;
    end.sin_addr.s_addr = htonl(INADDR_ANY);
    end.sin_port = htons(7070);

    if (bind(escuta, (struct sockaddr *)&end, sizeof end) < 0) {
        perror("bind");
        return 1;
    }
    if (listen(escuta, 16) < 0) {
        perror("listen");
        return 1;
    }
    printf("esperando na porta 7070\n");

    for (;;) {
        int con = accept(escuta, NULL, NULL);
        if (con < 0) {
            perror("accept");
            continue;
        }
        printf("conexao aceita\n");
        /* conversa com o cliente */
        close(con);
    }
}
