        .globl _start
        .text
_start:
        li   a0, 1
        la   a1, sigla
        li   a2, 3
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
sigla:  .ascii "PS\n"
