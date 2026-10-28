'diario' => [
    'driver' => 'daily',
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'info'),
    'formatter' => JsonFormatter::class,
    'days' => 30,
],
