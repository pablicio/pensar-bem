        .globl _start
        .text
_start:
        li   a0, 0              # de onde: o teclado
        la   a1, visor          # para onde: os dois bytes do visor
        li   a2, 1              # quantos: uma tecla
        li   a7, 63             # read
        ecall
        li   a0, 1
        la   a1, visor
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
visor:  .half 0
