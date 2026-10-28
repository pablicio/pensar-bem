public function boot(): void
{
    if ($this->app->isLocal()) {
        DB::listen(function (QueryExecuted $q) {
            if ($q->time > 100) {
                Log::channel('lentas')->warning('consulta lenta', [
                    'sql' => $q->sql,
                    'ms' => $q->time,
                ]);
            }
        });
    }
}
