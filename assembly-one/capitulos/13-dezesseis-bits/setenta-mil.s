        .globl _start
        .text
_start:
        li   t1, 70000
        la   t0, visor
        sh   t1, 0(t0)          # só cabem 16 bits
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
visor:  .half 0
