public function __invoke(Request $request)
{
    return new UsuarioResource(
        $request->user()->load('leitor'),
    );
}
