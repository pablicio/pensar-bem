use Illuminate\Support\Facades\Schedule;

Schedule::command('biblioteca:multas')
    ->dailyAt('03:00')
    ->withoutOverlapping();
