final class EmprestimoRealizado implements ShouldDispatchAfterCommit
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public readonly Emprestimo $emprestimo,
    ) {}
}
