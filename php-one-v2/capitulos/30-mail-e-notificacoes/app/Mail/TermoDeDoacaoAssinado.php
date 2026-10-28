final class TermoDeDoacaoAssinado extends Mailable implements
    ShouldQueue
{
    use Queueable, SerializesModels;

    public function __construct(public readonly Doacao $doacao) {}

    public function envelope(): Envelope
    {
        return new Envelope(subject: 'Seu termo de doação');
    }

    public function content(): Content
    {
        return new Content(markdown: 'mail.termo');
    }

    public function attachments(): array
    {
        return [
            Attachment::fromStorageDisk('local', $this->doacao->termo)
                ->as('termo-de-doacao.pdf')
                ->withMime('application/pdf'),
        ];
    }
}
