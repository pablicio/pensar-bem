        .globl _start
        .text
_start:
        la   t0, fichas
        la   t1, cores
        li   t2, 3
        li   s3, 4
        li   s4, 0
laco:
        blez t2, fim
        lbu  t3, 0(t1)
        bgt  t3, s3, proximo
        mv   s3, t3
        lh   s4, 0(t0)
proximo:
        addi t0, t0, 2
        addi t1, t1, 1
        addi t2, t2, -1
        j    laco
fim:
        la   t0, proxima
        sh   s4, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
fichas:  .half 301, 302, 303
cores:   .byte 3, 1, 1
        .align 1
proxima: .half 0
