use Illuminate\Database\Eloquent\Builder;

public function scopeEmAberto(Builder $q): void
{
    $q->whereNull('devolvido_em');
}

public function scopeVencidos(Builder $q): void
{
    $q->whereDate('devolver_ate', '<', now());
}
