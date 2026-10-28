        .globl _start
        .text
_start:
        la   s0, cauda
        la   s1, novas
        li   s2, 3
        la   s3, fila_fim
laco:
        blez s2, mostra
        ld   t0, 0(s0)
        bgeu t0, s3, cheia      # cauda chegou ao fim da fila?
        lh   t1, 0(s1)
        sh   t1, 0(t0)
        addi t0, t0, 2
        sd   t0, 0(s0)
        addi s1, s1, 2
        addi s2, s2, -1
        j    laco
mostra:
        li   a0, 1
        la   a1, fila
        li   a2, 8
        li   a7, 64
        ecall
        j    sai
cheia:
        li   a0, 1
        la   a1, erro
        li   a2, 2
        li   a7, 64
        ecall
sai:
        li   a0, 0
        li   a7, 93
        ecall

        .data
fila:     .half 214, 215, 219, 0
fila_fim:
cauda:    .dword fila + 6
novas:    .half 230, 241, 250
erro:     .half 9999
