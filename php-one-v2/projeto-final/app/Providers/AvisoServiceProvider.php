<?php

declare(strict_types=1);

namespace App\Providers;

use App\Avisos\EnviadorDeAviso;
use App\Avisos\EnviadorDeWhatsApp;
use App\Avisos\ClienteDoProvedor;
use Illuminate\Support\ServiceProvider;

class AvisoServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(
            ClienteDoProvedor::class,
            fn () => new ClienteDoProvedor(
                url: config('avisos.url'),
                chave: config('avisos.chave'),
                timeout: config('avisos.timeout', 5),
            ),
        );

        $this->app->bind(
            EnviadorDeAviso::class,
            EnviadorDeWhatsApp::class,
        );
    }
}
