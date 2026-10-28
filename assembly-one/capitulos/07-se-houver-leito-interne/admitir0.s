        .globl _start
        .text
_start:
        la   t0, livres
        lh   t1, 0(t0)
        blez t1, sem_leito
        addi t1, t1, -1
        sh   t1, 0(t0)
        lh   t2, 2(t0)
        addi t2, t2, 1
        sh   t2, 2(t0)
        j    fim
sem_leito:
        lh   t2, 4(t0)
        addi t2, t2, 1
        sh   t2, 4(t0)
fim:
        li   a0, 1
        la   a1, livres
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
livres:   .half 0
ocupados: .half 31
na_fila:  .half 0
