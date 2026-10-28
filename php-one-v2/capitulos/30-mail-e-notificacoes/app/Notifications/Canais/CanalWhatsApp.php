final class CanalWhatsApp
{
    public function __construct(
        private readonly EnviadorDeAviso $avisos,
    ) {}

    public function send(Leitor $leitor, Notification $aviso): void
    {
        $this->avisos->enviar($leitor, $aviso->toWhatsApp($leitor));
    }
}
