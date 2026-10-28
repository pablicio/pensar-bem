        .globl _start
        .text
_start:
        li   a0, 1              # para onde: a saída do programa
        la   a1, mensagem       # de onde: o endereço dos bytes
        li   a2, 3              # quantos bytes
        li   a7, 64             # pedido ao Linux: escrever
        ecall
        li   a0, 0
        li   a7, 93             # pedido ao Linux: terminar
        ecall

        .data
mensagem: .ascii "OI\n"
