public function scopeVisivelPara(Builder $q, Usuario $u): void
{
    if ($u->papel === Papel::Leitor) {
        $q->where('leitor_id', $u->leitor_id);
    }
}
