        .globl _start
        .text
_start:
inicio:
        li   a0, 0
        la   a1, tecla
        li   a2, 1
        li   a7, 63
        ecall
        blez a0, desliga
        la   t0, tecla
        lbu  t0, 0(t0)
        addi t0, t0, -49        # tecla 1 vira índice 0
        li   t1, 5
        bgeu t0, t1, invalida   # índice fora de 0..4?
        slli t0, t0, 3          # índice * 8: endereços têm 8 bytes
        la   t1, tabela
        add  t1, t1, t0
        ld   t2, 0(t1)          # o endereço do tratamento
        jr   t2                 # salta para ele
interna:
        li   t3, 100
        j    exibe
alta:
        li   t3, 200
        j    exibe
transf:
        li   t3, 300
        j    exibe
triagem:
        li   t3, 400
        j    exibe
chamar:
        li   t3, 500
        j    exibe
invalida:
        li   t3, 9998
exibe:
        la   t0, visor
        sh   t3, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        j    inicio
desliga:
        li   a0, 0
        li   a7, 93
        ecall

        .data
tabela: .dword interna          # tecla 1
        .dword alta             # tecla 2
        .dword transf           # tecla 3
        .dword triagem          # tecla 4
        .dword chamar           # tecla 5
visor:  .half 0
tecla:  .byte 0
