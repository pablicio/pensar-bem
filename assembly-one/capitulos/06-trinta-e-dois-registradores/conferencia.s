        .globl _start
        .text
_start:
        la   t0, dados
        lh   t1, 2(t0)          # ocupados
        lh   t2, 4(t0)
        add  t1, t1, t2
        lh   t2, 6(t0)
        add  t1, t1, t2         # t1 = indisponíveis
        lh   t2, 0(t0)          # t2 = leitos
        sub  t3, t2, t1         # t3 = livres
        add  t4, t3, t1         # t4 = livres + indisponíveis
        sh   t3, 8(t0)
        sh   t1, 10(t0)
        sh   t4, 12(t0)
        li   a0, 1
        addi a1, t0, 8
        li   a2, 6              # três meias-palavras
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
dados:  .half 40, 31, 3, 2      # leitos, ocup., bloq., reserv.
        .half 0, 0, 0           # livres, indisponíveis, conferência
