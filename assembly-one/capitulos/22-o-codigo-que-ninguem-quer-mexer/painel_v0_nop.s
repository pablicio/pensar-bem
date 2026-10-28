        .globl _start
        .text
_start:
        nop
        li   x5, 0x11128
        lh   x6, 0(x5)
        lh   x7, 2(x5)
        sub  x6, x6, x7
        bgez x6, 1f
        li   x6, 0
1:      sh   x6, 4(x5)
        li   x10, 1
        addi x11, x5, 4
        li   x12, 2
        li   x17, 64
        ecall
        li   x10, 0
        li   x17, 93
        ecall
        .data
        .half 40, 38, 0
