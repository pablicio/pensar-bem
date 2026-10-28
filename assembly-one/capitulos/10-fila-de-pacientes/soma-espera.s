        .globl _start
        .text
_start:
        la   t0, espera
        li   t4, 4
        li   t3, 0              # total
laco:
        blez t4, fim
        lh   t1, 0(t0)
        add  t3, t3, t1
        addi t0, t0, 2
        addi t4, t4, -1
        j    laco
fim:
        la   t0, total
        sh   t3, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
espera: .half 40, 25, 10, 5
total:  .half 0
