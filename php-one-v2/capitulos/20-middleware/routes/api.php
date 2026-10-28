Route::post('auth/login', LoginController::class)
    ->middleware('throttle:login');

Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('emprestimos', EmprestimoController::class);
});
