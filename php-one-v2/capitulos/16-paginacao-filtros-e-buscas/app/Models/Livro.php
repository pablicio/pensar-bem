public function scopeOrdenarPor(Builder $q, string $ordem): void
{
    match ($ordem) {
        'titulo' => $q->orderBy('titulo'),
        '-titulo' => $q->orderByDesc('titulo'),
        'ano' => $q->orderBy('ano'),
        '-ano' => $q->orderByDesc('ano'),
        'recentes' => $q->orderByDesc('created_at'),
    };

    $q->orderBy('id');
}
