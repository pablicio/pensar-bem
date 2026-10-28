# Painel de leitos e fila do PS — Hospital Santa Byte
# Vetor Sistemas, dezembro de 2026. Placa LabArq Painel RV64 rev. 2.
# Teclas: 1 internação, 2 alta, 3 transferência recebida,
#         4 triagem (depois: ficha#, cor#, idade#), 5 chamar.
# Ao ligar: mostra 0 e espera os ocupados do quadro, com #.
# Display: 9999 confira o quadro; 9998 tecla inválida;
#          9997 fila cheia; 9996 sem leito livre.
# Versão 2, 8/12/2026: os testes da Cida.
        .equ LEITOS, 40
        .equ CAPACIDADE, 20     # maior fila registrada: 9 (nov/2026)

        .globl _start
        .text
# ---- ao ligar: a Cida digita os ocupados do quadro ----
_start:
        li   a0, 0
        call mostra             # 00000: esperando o número
pergunta:
        call le_numero
        li   t0, -2
        beq  a0, t0, desliga    # só na bancada: o teclado acabou
        bltz a0, pergunta_erro
        li   t0, LEITOS
        bgt  a0, t0, pergunta_erro
        la   t0, ocupados
        sh   a0, 0(t0)
        call mostra_livres
        j    laco
pergunta_erro:
        li   a0, 9998
        call mostra
        j    pergunta
# ---- laço principal: lê a tecla, confere, despacha ----
laco:
        li   a0, 0
        la   a1, tecla
        li   a2, 1
        li   a7, 63             # read
        ecall
        blez a0, desliga        # só na bancada: o teclado acabou
        la   t0, tecla
        lbu  t0, 0(t0)
        addi t0, t0, -49        # tecla 1 vira índice 0
        li   t1, 5
        bgeu t0, t1, invalida
        slli t0, t0, 3
        la   t1, tabela
        add  t1, t1, t0
        ld   t2, 0(t1)
        jr   t2
# ---- teclas 1, 2 e 3: leitos ----
interna:
transf:
        la   t0, ocupados
        lh   t1, 0(t0)
        li   t2, LEITOS
        bge  t1, t2, lotado     # sem leito: recusa sem contar
        addi t1, t1, 1
        sh   t1, 0(t0)
        call mostra_livres
        j    laco
alta:
        la   t0, ocupados
        lh   t1, 0(t0)
        blez t1, invalida       # ninguém para dar alta
        addi t1, t1, -1
        sh   t1, 0(t0)
        call mostra_livres
        j    laco
# ---- tecla 4: triagem ----
triagem:
        call le_numero          # ficha
        bltz a0, invalida
        mv   s1, a0
        call le_numero          # cor
        bltz a0, invalida
        mv   s2, a0
        call le_numero          # idade
        bltz a0, invalida
        mv   s3, a0
        beqz s1, invalida       # ficha 0 é reservada: fila vazia
        li   t0, 9999
        bgt  s1, t0, invalida   # ficha de 1 a 9999
        li   t0, 1              # a cor precisa ser 1, 3 ou 4
        beq  s2, t0, tr_cabe
        li   t0, 4
        beq  s2, t0, tr_cabe
        li   t0, 3
        bne  s2, t0, invalida
        li   t0, 80             # amarelo com 80 ou mais vira 2
        blt  s3, t0, tr_cabe
        li   s2, 2
tr_cabe:
        la   t0, quant
        lh   t1, 0(t0)
        li   t2, CAPACIDADE
        bge  t1, t2, cheia
        la   t3, fichas
        slli t4, t1, 1
        add  t3, t3, t4
        sh   s1, 0(t3)
        la   t3, cores
        add  t3, t3, t1
        sb   s2, 0(t3)
        addi t1, t1, 1
        sh   t1, 0(t0)
        call mostra_proximo
        j    laco
# ---- tecla 5: chamar o próximo ----
chamar:
        call procura            # a0 = posição; -1: fila vazia
        bltz a0, ch_mostra
        call remove
ch_mostra:
        call mostra_proximo
        j    laco
# ---- avisos ----
invalida:
        li   a0, 9998
        call mostra
        j    laco
cheia:
        li   a0, 9997
        call mostra
        j    laco
lotado:
        li   a0, 9996
        call mostra
        j    laco
desliga:
        li   a0, 0
        li   a7, 93
        ecall

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
        li   a7, 64             # write
        ecall
        ret

# ---- le_numero: lê algarismos até o # ----
# entra:  nada (lê do teclado)
# sai:    a0 = o número; -1 se veio * ou outra tecla; -2 se o
#         teclado acabou (só na bancada)
# altera: a0, a1, a2, a7, t0 a t3
le_numero:
        li   t3, 0
ln_tecla:
        li   a0, 0
        la   a1, tecla
        li   a2, 1
        li   a7, 63
        ecall
        blez a0, ln_acabou
        la   t0, tecla
        lbu  t1, 0(t0)
        li   t2, 35             # #: confirma
        beq  t1, t2, ln_pronto
        addi t1, t1, -48
        li   t2, 10
        bgeu t1, t2, ln_cancela # não é algarismo: * ou outra
        mul  t3, t3, t2
        add  t3, t3, t1
        j    ln_tecla
ln_pronto:
        mv   a0, t3
        ret
ln_cancela:
        li   a0, -1
        ret
ln_acabou:
        li   a0, -2
        ret

# ---- mostra_livres: sanidade e leitos livres no display ----
# entra:  nada (lê ocupados da memória)
# sai:    display com os livres, ou 9999
# altera: a0, a1, a2, a7, t0, t1
mostra_livres:
        addi sp, sp, -16
        sd   ra, 8(sp)
        la   t0, ocupados
        lh   t1, 0(t0)
        li   a0, LEITOS
        sub  a0, a0, t1
        bltz a0, ml_falha
        li   t1, LEITOS
        ble  a0, t1, ml_exibe
ml_falha:
        li   a0, 9999
ml_exibe:
        call mostra
        ld   ra, 8(sp)
        addi sp, sp, 16
        ret

# ---- procura: a menor cor; no empate, quem chegou antes ----
# entra:  nada (lê a fila da memória)
# sai:    a0 = posição do próximo, desde 0 (-1 se a fila está vazia)
#         a1 = a ficha dele (0 se a fila está vazia)
# altera: a0, a1, t0 a t5
procura:
        la   t0, quant
        lh   t1, 0(t0)
        li   a0, -1
        li   a1, 0
        li   t2, 5              # melhor cor: pior que qualquer real
        li   t3, 0              # posição atual
pr_laco:
        bge  t3, t1, pr_fim
        la   t4, cores
        add  t4, t4, t3
        lbu  t5, 0(t4)
        bge  t5, t2, pr_prox    # não é estritamente mais urgente
        mv   t2, t5
        mv   a0, t3
        la   t4, fichas
        slli t5, t3, 1
        add  t4, t4, t5
        lh   a1, 0(t4)
pr_prox:
        addi t3, t3, 1
        j    pr_laco
pr_fim:
        ret

# ---- remove: tira a posição a0, sem mudar a ordem ----
# entra:  a0 = posição (0 <= a0 < quant)
# sai:    fila com um a menos, mesma ordem de chegada
# altera: t0 a t5
remove:
        la   t0, quant
        lh   t1, 0(t0)
        addi t1, t1, -1         # o último índice
        mv   t2, a0
re_laco:
        bge  t2, t1, re_fim     # enquanto posição < último
        la   t3, fichas         # fichas[i] = fichas[i + 1]
        slli t4, t2, 1
        add  t3, t3, t4
        lh   t5, 2(t3)
        sh   t5, 0(t3)
        la   t3, cores          # cores[i] = cores[i + 1]
        add  t3, t3, t2
        lbu  t5, 1(t3)
        sb   t5, 0(t3)
        addi t2, t2, 1
        j    re_laco
re_fim:
        sh   t1, 0(t0)          # quant - 1
        ret

# ---- mostra_proximo: a ficha de quem é o próximo ----
# entra:  nada
# sai:    display com a ficha, ou 0 se a fila está vazia
# altera: o mesmo que procura e mostra
mostra_proximo:
        addi sp, sp, -16
        sd   ra, 8(sp)
        call procura
        mv   a0, a1
        call mostra
        ld   ra, 8(sp)
        addi sp, sp, 16
        ret

        .data
tabela:   .dword interna, alta, transf, triagem, chamar
ocupados: .half 0               # a Cida digita ao ligar
quant:    .half 0               # pacientes na fila
visor:    .half 0
tecla:    .byte 0

        .bss                    # a fila: zerada ao ligar
        .align 1
fichas:   .space 2 * CAPACIDADE
cores:    .space CAPACIDADE
