public function livro(): BelongsTo
{
    return $this->belongsTo(Livro::class);
}
