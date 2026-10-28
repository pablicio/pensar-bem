if ($this->app->environment('local')) {
    DB::listen(function ($consulta): void {
        Log::debug($consulta->sql, [
            'valores' => $consulta->bindings,
            'ms' => $consulta->time,
        ]);
    });
}
