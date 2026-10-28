<?php

declare(strict_types=1);

final class Registro
{
    public function __construct(private string $arquivo)
    {
    }

    public function info(string $mensagem, array $contexto = []): void
    {
        $this->gravar('info', $mensagem, $contexto);
    }

    public function erro(string $mensagem, array $contexto = []): void
    {
        $this->gravar('error', $mensagem, $contexto);
    }

    private function gravar(
        string $nivel,
        string $msg,
        array $ctx,
    ): void
    {
        $linha = json_encode([
            'quando' => date(DATE_ATOM),
            'nivel' => $nivel,
            'mensagem' => $msg,
            'contexto' => $ctx,
        ], JSON_UNESCAPED_UNICODE);

        file_put_contents(
            $this->arquivo,
            $linha . "\n",
            FILE_APPEND | LOCK_EX,
        );
    }
}
