<?php

$senha_enviada = md5($_POST['senha']);

if ($senha_enviada == $senha_guardada) {
    entrar();
}
