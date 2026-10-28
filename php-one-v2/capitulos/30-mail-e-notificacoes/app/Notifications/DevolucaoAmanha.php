final class DevolucaoAmanha extends Notification implements
    ShouldQueue
{
    use Queueable;

    public function __construct(
        public readonly Emprestimo $emprestimo,
    ) {
        $this->afterCommit();
    }

    public function via(Leitor $leitor): array
    {
        return array_values(array_filter([
            $leitor->email !== null ? 'mail' : null,
            $leitor->aceita_whatsapp ? CanalWhatsApp::class : null,
            'database',
        ]));
    }

    public function toMail(Leitor $leitor): MailMessage
    {
        $titulo = $this->emprestimo->exemplar->livro->titulo;

        return (new MailMessage)
            ->subject("\"{$titulo}\" vence amanhã")
            ->greeting("Olá, {$leitor->nome}!")
            ->line("O prazo de \"{$titulo}\" termina amanhã.")
            ->line('Se precisar de mais tempo, dá para renovar.')
            ->action('Renovar', $this->linkDeRenovacao());
    }

    public function toWhatsApp(Leitor $leitor): string
    {
        return sprintf(
            '"%s" vence amanhã. Renove pelo aplicativo.',
            $this->emprestimo->exemplar->livro->titulo,
        );
    }

    public function toArray(Leitor $leitor): array
    {
        return [
            'emprestimo_id' => $this->emprestimo->id,
            'devolver_ate' => $this->emprestimo->devolver_ate
                ->toDateString(),
        ];
    }
}
