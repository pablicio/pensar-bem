        .globl _start
        .text
_start:
        la   s0, numero
        li   t4, 3              # início
laco:
        blez t4, fim
        sh   t4, 0(s0)          # o próprio contador é o que se mostra
        li   a0, 1
        mv   a1, s0
        li   a2, 2
        li   a7, 64
        ecall
        addi t4, t4, -1
        j    laco
fim:
        li   a0, 0
        li   a7, 93
        ecall

        .data
numero: .half 0
