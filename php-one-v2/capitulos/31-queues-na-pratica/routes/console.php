Schedule::command('queue:monitor', [
    'database:avisos,database:default', '--max' => 50,
])->everyFiveMinutes();
