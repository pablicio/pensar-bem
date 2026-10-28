        .globl _start
        .text
_start:
        la   t0, total
        lwu  t1, 0(t0)
        addi t1, t1, 1
        sw   t1, 0(t0)
        li   t2, 1000
        divu t3, t1, t2
        remu t4, t1, t2
        sh   t3, 4(t0)
        sh   t4, 6(t0)
        li   a0, 1
        addi a1, t0, 4
        li   a2, 4
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
total:    .word 999999
milhares: .half 0
unidades: .half 0
