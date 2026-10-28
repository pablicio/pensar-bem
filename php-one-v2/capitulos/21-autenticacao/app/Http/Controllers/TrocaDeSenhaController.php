public function __invoke(
    TrocaDeSenhaRequest $request,
    ConferidorDeSenha $conferidor,
) {
    $usuario = $request->user();

    if (!$conferidor->confere($usuario, $request->senha_atual)) {
        throw new CredenciaisInvalidas();
    }

    $usuario->senha = $request->senha_nova;
    $usuario->save();

    $atual = $usuario->currentAccessToken()->id;

    $usuario->tokens()
        ->where('id', '!=', $atual)
        ->delete();

    return response()->noContent();
}
