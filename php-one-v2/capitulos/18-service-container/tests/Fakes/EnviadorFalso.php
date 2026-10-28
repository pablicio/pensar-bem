final class EnviadorFalso implements EnviadorDeAviso
{
    public array $enviados = [];

    public function enviar(Leitor $leitor, string $texto): void
    {
        $this->enviados[] = [
            'leitor' => $leitor->id,
            'texto' => $texto,
        ];
    }
}
