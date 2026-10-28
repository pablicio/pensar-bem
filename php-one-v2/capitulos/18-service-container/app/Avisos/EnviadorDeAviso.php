interface EnviadorDeAviso
{
    public function enviar(Leitor $leitor, string $texto): void;
}
