public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
