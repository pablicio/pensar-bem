public function middleware(object $leitor, string $canal): array
{
    return $canal === CanalWhatsApp::class
        ? [new RateLimited('whatsapp')]
        : [];
}

public function retryUntil(): DateTime
{
    return now()->addHours(3);
}
