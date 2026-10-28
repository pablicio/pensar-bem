RateLimiter::for('whatsapp', fn () => Limit::perMinute(60));
