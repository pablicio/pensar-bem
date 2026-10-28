        .globl _start
        .text
_start:
        la   s0, fila           # ponteiro: a primeira ficha
        li   s1, 4              # contador: quantas fichas
laco:
        blez s1, fim
        li   a0, 1              # mostra a ficha apontada
        mv   a1, s0
        li   a2, 2
        li   a7, 64
        ecall
        addi s0, s0, 2          # anda com o ponteiro: dois bytes
        addi s1, s1, -1
        j    laco
fim:
        li   a0, 0
        li   a7, 93
        ecall

        .data
fila:   .half 214, 215, 219, 230
