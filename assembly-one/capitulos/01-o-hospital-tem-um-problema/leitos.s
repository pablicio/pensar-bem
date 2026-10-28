        .globl _start
        .text
_start:
        li   a0, 40             # o número de leitos
        li   a7, 93             # pedido ao Linux: terminar
        ecall                   # faça o pedido
