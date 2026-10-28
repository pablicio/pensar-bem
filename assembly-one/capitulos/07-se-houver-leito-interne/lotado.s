        .globl _start
        .text
_start:
        la   t0, livres
        lh   t1, 0(t0)
        bnez t1, tem_leito      # livres != 0: não está lotado
        li   t2, 1              # lotado
        j    fim
tem_leito:
        li   t2, 0
fim:
        sh   t2, 2(t0)          # resposta
        li   a0, 1
        addi a1, t0, 2
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
livres:   .half 0
resposta: .half 0
