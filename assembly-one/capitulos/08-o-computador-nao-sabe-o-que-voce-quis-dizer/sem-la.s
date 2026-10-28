        .globl _start
        .text
_start:
        lh   t1, 0(t0)          # t0 nunca recebeu um endereço
        li   a0, 0
        li   a7, 93
        ecall
