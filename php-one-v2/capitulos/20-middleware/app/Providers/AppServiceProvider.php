public function boot(): void
{
    RateLimiter::for('login', function (Request $request) {
        return [
            Limit::perMinute(5)->by(
                mb_strtolower((string) $request->input('email'))
                    . '|' . $request->ip(),
            ),
            Limit::perMinute(30)->by($request->ip()),
        ];
    });
}
