        .globl _start
        .text
_start:
        call mostra_livres
        li   a0, 0
        li   a7, 93
        ecall

# ---- mostra_livres: os leitos livres no display ----
# entra:  nada (lê leitos e ocupados da memória)
# sai:    nada
# altera: a0, a1, a2, a7, t0
mostra_livres:
        addi sp, sp, -16        # abre 16 bytes na pilha
        sd   ra, 8(sp)          # guarda a volta
        la   t0, dados
        lh   a0, 0(t0)
        lh   a1, 2(t0)
        call calcula_livres
        call mostra
        ld   ra, 8(sp)          # recupera a volta
        addi sp, sp, 16         # fecha o espaço
        ret

calcula_livres:
        sub  t0, a0, a1
        bltz t0, cl_falha
        bgt  t0, a0, cl_falha
        mv   a0, t0
        ret
cl_falha:
        li   a0, 9999
        ret

mostra:
        la   t0, visor
        sh   a0, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        ret

        .data
dados:  .half 40, 31
visor:  .half 0
