public function __invoke(Request $request)
{
    $request->user()->currentAccessToken()->delete();

    return response()->noContent();
}
