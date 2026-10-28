        .globl _start
        .text
_start:
        la   t0, espera
        li   t2, 4
        li   s3, -1             # menor que qualquer espera real
laco:
        blez t2, fim
        lh   t3, 0(t0)
        ble  t3, s3, proximo    # não é maior: segue
        mv   s3, t3
proximo:
        addi t0, t0, 2
        addi t2, t2, -1
        j    laco
fim:
        la   t0, maior
        sh   s3, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
espera: .half 40, 25, 70, 5
maior:  .half 0
