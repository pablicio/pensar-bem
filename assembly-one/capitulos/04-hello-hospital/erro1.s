        .globl _start
        .text
_start:
        li   a0, 1
        la   a1, mensagem
        lii  a2, 3
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
mensagem: .ascii "OI\n"
