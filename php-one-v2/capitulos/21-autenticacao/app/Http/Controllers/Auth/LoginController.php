public function __invoke(
    LoginRequest $request,
    ConferidorDeSenha $conferidor,
) {
    $usuario = Usuario::where(
        'email',
        mb_strtolower($request->string('email')),
    )->first();

    $valido = $usuario !== null
        && $conferidor->confere($usuario, $request->senha);

    if (!$usuario) {
        Hash::check($request->senha, self::HASH_FALSO);
    }

    if (!$valido) {
        throw new CredenciaisInvalidas();
    }

    $token = $usuario->createToken(
        name: $request->string('dispositivo', 'app'),
        abilities: $usuario->papel->habilidades(),
        expiresAt: now()->addDays(30),
    );

    return response()->json([
        'token' => $token->plainTextToken,
        'expira_em' => $token->accessToken->expires_at
            ->toIso8601String(),
        'usuario' => new UsuarioResource($usuario),
    ], 201);
}
