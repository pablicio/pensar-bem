        .globl _start
        .text
_start:
        la   t0, dados
        lh   a0, 0(t0)          # leitos
        lh   a1, 2(t0)          # ocupados
        call calcula_livres
        call mostra             # a0 já tem o que mostrar
        li   a0, 0
        li   a7, 93
        ecall

# ---- calcula_livres: leitos livres, com sanidade ----
# entra:  a0 = leitos, a1 = ocupados
# sai:    a0 = livres, ou 9999 se o número for impossível
# altera: a0, t0
calcula_livres:
        sub  t0, a0, a1
        bltz t0, cl_falha
        bgt  t0, a0, cl_falha
        mv   a0, t0
        ret
cl_falha:
        li   a0, 9999
        ret

# ---- mostra: escreve um número no display ----
# entra:  a0 = o número (os 16 bits de baixo)
# sai:    nada
# altera: a0, a1, a2, a7, t0
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
dados:  .half 40, 31            # leitos, ocupados
visor:  .half 0
