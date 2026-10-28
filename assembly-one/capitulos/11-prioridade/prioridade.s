        .globl _start
        .text
_start:
        la   t0, fichas         # ficha atual
        la   t1, cores          # cor atual
        li   t2, 4              # quantos
        li   s3, 4              # melhor cor: pior que qualquer real
        li   s4, 0              # melhor ficha: 0 quer dizer ninguém
laco:
        blez t2, fim
        lbu  t3, 0(t1)          # cor do paciente atual
        bge  t3, s3, proximo    # não é mais urgente: segue
        mv   s3, t3             # novo melhor
        lh   s4, 0(t0)
proximo:
        addi t0, t0, 2          # os dois ponteiros andam juntos,
        addi t1, t1, 1          # cada um com o tamanho do seu item
        addi t2, t2, -1
        j    laco
fim:
        la   t0, proxima
        sh   s4, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
fichas:  .half 214, 215, 219, 230   # por ordem de chegada
cores:   .byte 3, 2, 3, 1           # 1 vermelho, 2 amarelo, 3 verde
proxima: .half 0
