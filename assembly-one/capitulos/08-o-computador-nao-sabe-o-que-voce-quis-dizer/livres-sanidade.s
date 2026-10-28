        .globl _start
        .text
_start:
        la   t0, dados
        lh   t1, 0(t0)          # leitos
        lh   t2, 2(t0)          # ocupados
        sub  t3, t1, t2         # livres
        bltz t3, falha          # livres negativo?
        bgt  t3, t1, falha      # livres maior que leitos?
        j    mostra
falha:
        li   t3, 9999
mostra:
        sh   t3, 4(t0)
        li   a0, 1
        addi a1, t0, 4
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
dados:  .half 40
        .half 45
        .half 0
