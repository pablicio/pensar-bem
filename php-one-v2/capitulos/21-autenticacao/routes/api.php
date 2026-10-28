Route::post('auth/login', LoginController::class)
    ->middleware('throttle:login');

Route::middleware('auth:sanctum')->group(function () {
    Route::get('eu', EuController::class);
    Route::post('auth/logout', LogoutController::class);
    // ... o resto da API do leitor
});
