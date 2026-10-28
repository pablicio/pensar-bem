$this->app->bind(
    EnviadorDeAviso::class,
    $this->app->isProduction()
        ? EnviadorDeWhatsApp::class
        : EnviadorNoLog::class,
);
