        .globl _start
        .text
_start:
        la   t0, dados
        lh   t1, 0(t0)          # leitos
        lh   t2, 2(t0)          # ocupados
        sub  t3, t1, t2
        sh   t3, 8(t0)          # disponíveis da observação
        lh   t1, 4(t0)          # leitos da UTI
        lh   t2, 6(t0)          # ocupados da UTI
        sub  t3, t1, t2
        sh   t3, 10(t0)         # livres da UTI
        li   a0, 1
        addi a1, t0, 8
        li   a2, 4              # as duas meias-palavras
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
dados:  .half 40                # 0  leitos
        .half 33                # 2  ocupados
        .half 12                # 4  leitos da UTI
        .half 9                 # 6  ocupados da UTI
        .half 0                 # 8  disponíveis
        .half 0                 # 10 livres da UTI
