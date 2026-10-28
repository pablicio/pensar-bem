#!/bin/sh
# testes.sh: os casos da Cida e o roteiro do plantão.
# uso: sh testes.sh painel-v2.s
programa=${1:-painel-v2.s}
falhas=0
caso() {        # caso "nome" "teclas" "o que o display deve mostrar"
    obtido=$(printf '%s' "$2" | roda "$programa" | display |
             tr '\n' ' ')
    if [ "$obtido" = "$3 " ]; then
        echo "ok     $1"
    else
        echo "FALHA  $1"
        echo "       esperado: $3"
        echo "       obtido:   $obtido"
        falhas=$((falhas + 1))
    fi
}
caso "lotado, chega paciente"   '40#1' '00000 00000 09996'
caso "lotado, transferência"    '40#3' '00000 00000 09996'
caso "vazio, tecla de alta"     '0#2'  '00000 00040 09998'
caso "ficha 0 na triagem"       '37#40#4#10#'      '00000 00003 09998'
caso "prontuário no lugar da ficha" '37#4123456#3#40#' \
     '00000 00003 09998'
caso "cancela a triagem com *"  '37#41*1' '00000 00003 09998 00002'
caso "tecla 7"                  '37#7' '00000 00003 09998'
vinte=$(for i in $(seq 101 121); do printf '4%d#4#30#' "$i"; done)
caso "fila com 20, chega o 21º" "37#$vinte" \
     "00000 00003 $(printf '00101 %.0s' $(seq 20))09997"
teclas='37#14214#4#30#4219#3#82#4230#1#60#555527'
e1='00000 00003 00002 00214 00219 00230'
e2='00219 00214 00000 00000 00003 09998'
caso "roteiro do plantão" "$teclas" "$e1 $e2"
echo "$falhas falhas"
