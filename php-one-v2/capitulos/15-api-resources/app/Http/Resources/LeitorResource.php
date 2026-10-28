public function toArray(Request $request): array
{
    $proprio = $request->user()?->leitor_id === $this->id;
    $equipe = $request->user()?->ehEquipe() ?? false;

    return [
        'id' => $this->id,
        'nome' => $this->nome,
        'telefone' => $this->when(
            $proprio || $equipe,
            $this->telefone,
        ),
        'documento' => $this->when($equipe, $this->documento),
        'membro_desde' => $this->created_at->toDateString(),
    ];
}
