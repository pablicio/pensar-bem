final class ExemplarDevolvido implements ShouldDispatchAfterCommit
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public readonly Exemplar $exemplar,
    ) {}
}
