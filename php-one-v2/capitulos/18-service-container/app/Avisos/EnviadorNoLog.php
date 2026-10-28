final class EnviadorNoLog implements EnviadorDeAviso
{
    public function enviar(Leitor $leitor, string $texto): void
    {
        Log::info('aviso', [
            'leitor' => $leitor->id,
            'texto' => $texto,
        ]);
    }
}
